#!/usr/bin/env python
"""
UsabilityUniverse Game Server - Independent server for usability principle identification game
Completely separate from QualityQuest and RequirementRally to avoid breaking existing functionality
"""

import sys
import os
import traceback
import uuid
import json
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    print("Python version:", sys.version)
    print("Python executable:", sys.executable)
    
    print("Importing required modules...")
    
    # FastAPI and related imports
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
    
    # Import the usability scenarios database
    from usability_scenarios_db import get_random_scenarios, get_database_stats, validate_scenarios
    
    print("All modules imported successfully")
    
    # Pydantic models for UsabilityUniverse
    class UniverseSessionCreateRequest(BaseModel):
        name: str
        category: Optional[str] = None  # 'Learnability', 'Efficiency', 'Memorability', 'Error_Prevention', 'User_Satisfaction', or None for mixed
        difficulty: Optional[str] = None  # 'easy', 'medium', 'hard', or None for mixed
        language: str = 'en'  # Default to English
        scenario_count: int = 5

    class UniverseAnswerRequest(BaseModel):
        session_id: str
        scenario_index: int
        selected_answer: str
        time_taken: Optional[float] = None

    class UniverseSessionResponse(BaseModel):
        id: str
        current_scenario: Dict[str, Any]
        total_scenarios: int
        current_index: int

    class UniverseAnswerResponse(BaseModel):
        correct: bool
        correct_answer: str
        feedback: str
        score: int
        next_scenario: Optional[Dict[str, Any]] = None
        game_completed: bool = False
        final_score: Optional[int] = None
        total_scenarios: Optional[int] = None

except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Traceback:")
    traceback.print_exc()
    sys.exit(1)

# FastAPI app
app = FastAPI(
    title="UsabilityUniverse Game Server",
    description="Independent server for usability principle identification game",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage (in production, use a proper database)
universe_sessions: Dict[str, Dict[str, Any]] = {}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "UsabilityUniverse Game Server", 
        "version": "1.0.0",
        "status": "running",
        "game": "usability_universe"
    }

@app.get("/universe/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "game": "usability_universe"
    }

@app.get("/universe/stats")
async def get_stats():
    """Get database statistics"""
    try:
        stats = get_database_stats()
        validation = validate_scenarios()
        
        return {
            "database_stats": stats,
            "validation": validation,
            "active_sessions": len(universe_sessions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.post("/universe/session", response_model=UniverseSessionResponse)
async def create_session(request: UniverseSessionCreateRequest):
    """Create a new game session"""
    try:
        print(f"Creating UsabilityUniverse session for player: {request.name}")
        print(f"Category: {request.category}, Difficulty: {request.difficulty}, Language: {request.language}")
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Get scenarios from database
        scenarios = get_random_scenarios(
            count=request.scenario_count,
            category=request.category,
            difficulty=request.difficulty,
            language=request.language
        )
        
        if not scenarios:
            raise HTTPException(
                status_code=404, 
                detail=f"No scenarios found for category: {request.category}, difficulty: {request.difficulty}"
            )
        
        # Create session
        session_data = {
            "id": session_id,
            "player_name": request.name,
            "category": request.category,
            "difficulty": request.difficulty,
            "language": request.language,
            "scenarios": scenarios,
            "current_index": 0,
            "score": 0,
            "answers": [],
            "created_at": datetime.now().isoformat(),
            "completed": False
        }
        
        universe_sessions[session_id] = session_data
        
        print(f"Session created with {len(scenarios)} scenarios")
        
        # Return current scenario
        current_scenario = scenarios[0] if scenarios else None
        
        return UniverseSessionResponse(
            id=session_id,
            current_scenario=current_scenario,
            total_scenarios=len(scenarios),
            current_index=0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating session: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@app.post("/universe/answer", response_model=UniverseAnswerResponse)
async def submit_answer(request: UniverseAnswerRequest):
    """Submit an answer for evaluation"""
    try:
        # Get session
        if request.session_id not in universe_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = universe_sessions[request.session_id]
        
        if session["completed"]:
            raise HTTPException(status_code=400, detail="Session already completed")
        
        # Validate scenario index
        if request.scenario_index != session["current_index"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid scenario index. Expected {session['current_index']}, got {request.scenario_index}"
            )
        
        # Get current scenario
        scenarios = session["scenarios"]
        if request.scenario_index >= len(scenarios):
            raise HTTPException(status_code=400, detail="Scenario index out of range")
        
        current_scenario = scenarios[request.scenario_index]
        correct_answer = current_scenario["correct_answer"]
        
        # Evaluate answer
        is_correct = request.selected_answer.lower() == correct_answer.lower()
        
        # Update score
        points = 10 if is_correct else 0
        session["score"] += points
        
        # Record answer
        answer_record = {
            "scenario_index": request.scenario_index,
            "scenario_id": current_scenario.get("id", f"scenario_{request.scenario_index}"),
            "selected_answer": request.selected_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "points": points,
            "time_taken": request.time_taken,
            "timestamp": datetime.now().isoformat()
        }
        session["answers"].append(answer_record)
        
        # Move to next scenario
        session["current_index"] += 1
        
        # Check if game completed
        game_completed = session["current_index"] >= len(scenarios)
        if game_completed:
            session["completed"] = True
            session["completed_at"] = datetime.now().isoformat()
        
        # Get next scenario
        next_scenario = None
        if not game_completed and session["current_index"] < len(scenarios):
            next_scenario = scenarios[session["current_index"]]
        
        print(f"Answer submitted: {is_correct}, Score: {session['score']}, Completed: {game_completed}")
        
        return UniverseAnswerResponse(
            correct=is_correct,
            correct_answer=correct_answer,
            feedback=current_scenario.get("feedback", "No feedback available"),
            score=session["score"],
            next_scenario=next_scenario,
            game_completed=game_completed,
            final_score=session["score"] if game_completed else None,
            total_scenarios=len(scenarios) if game_completed else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error submitting answer: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error submitting answer: {str(e)}")

@app.get("/universe/session/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id not in universe_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = universe_sessions[session_id]
    
    # Don't expose scenarios in session info (they should be requested individually)
    safe_session = {
        "id": session["id"],
        "player_name": session["player_name"],
        "category": session["category"],
        "difficulty": session["difficulty"],
        "language": session["language"],
        "current_index": session["current_index"],
        "score": session["score"],
        "total_scenarios": len(session["scenarios"]),
        "completed": session["completed"],
        "created_at": session["created_at"]
    }
    
    if session["completed"]:
        safe_session["completed_at"] = session.get("completed_at")
        safe_session["answers"] = session["answers"]
    
    return safe_session

@app.delete("/universe/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    if session_id not in universe_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del universe_sessions[session_id]
    return {"message": "Session deleted successfully"}

# Cleanup old sessions (simple cleanup - in production use proper job scheduling)
@app.on_event("startup")
async def startup_event():
    print("UsabilityUniverse Game Server starting up...")
    
    # Validate scenarios database
    try:
        validation = validate_scenarios()
        if not validation["is_valid"]:
            print("WARNING: Scenarios database validation failed:")
            for error in validation["errors"]:
                print(f"  ERROR: {error}")
        
        stats = get_database_stats()
        print(f"Loaded {stats['total_scenarios']} scenarios")
        print(f"Categories: {list(stats['categories'].keys())}")
        print(f"Languages: {stats['languages']}")
        
    except Exception as e:
        print(f"Error during startup validation: {e}")

async def cleanup_old_sessions():
    """Clean up sessions older than 24 hours"""
    try:
        current_time = datetime.now()
        to_delete = []
        
        for session_id, session in universe_sessions.items():
            created_at = datetime.fromisoformat(session["created_at"])
            age = current_time - created_at
            
            # Delete sessions older than 24 hours
            if age.total_seconds() > 24 * 60 * 60:
                to_delete.append(session_id)
        
        for session_id in to_delete:
            del universe_sessions[session_id]
            print(f"Cleaned up old session: {session_id}")
            
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    import uvicorn
    
    print("Starting UsabilityUniverse Game Server...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # Run server on port 8002 (different from RequirementRally on 8000)
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8002,
        log_level="info",
        reload=False  # Set to True for development
    )