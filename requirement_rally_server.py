#!/usr/bin/env python
"""
RequirementRally Game Server - Independent server for requirement type identification game
Completely separate from QualityQuest to avoid breaking existing functionality
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
    
    # Import LLM components
    from iso_standards_games.llm.provider import get_llm_provider
    from iso_standards_games.core.config import settings
    
    # Import the requirements scenarios database
    from requirements_scenarios_db import get_random_scenarios, get_database_stats, validate_scenarios
    
    print("All modules imported successfully")
    
    # Pydantic models for RequirementRally
    class RallySessionCreateRequest(BaseModel):
        name: str
        category: Optional[str] = None  # 'Functional', 'Non-Functional', 'Constraint', or None for mixed
        difficulty: Optional[str] = None  # 'easy', 'medium', 'hard', or None for mixed
        language: str = 'es'
    
    class RallyGameSession(BaseModel):
        id: str
        game_id: str = "requirement-rally"
        current_scenario: Dict[str, Any]
        status: str = "active"
        score: int = 0
        scenarios_completed: int = 0
        created_at: str
        category_filter: Optional[str] = None
        difficulty_filter: Optional[str] = None
    
    class RallyResponseSubmission(BaseModel):
        selected_option: str
    
    class RallyGameResponse(BaseModel):
        is_correct: bool
        correct_answer: str
        explanation: str
        score: int
        next_scenario: Optional[Dict[str, Any]] = None
        game_completed: bool = False
    
    print("Creating RequirementRally app...")
    
    # Create FastAPI app for RequirementRally
    app = FastAPI(title="RequirementRally Game API", version="1.0.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files for frontend
    frontend_path = os.path.join(os.path.dirname(__file__), "requirement-rally-frontend")
    if os.path.exists(frontend_path):
        # Mount static files but allow API routes to take precedence
        
        @app.get("/")
        async def read_index():
            return FileResponse(os.path.join(frontend_path, "index.html"))
            
        @app.get("/{file_path:path}")
        async def read_static_files(file_path: str):
            # Don't serve API routes as static files
            if file_path.startswith("rally/"):
                raise HTTPException(status_code=404, detail="Not found")
            
            file_location = os.path.join(frontend_path, file_path)
            if os.path.exists(file_location) and os.path.isfile(file_location):
                return FileResponse(file_location)
            raise HTTPException(status_code=404, detail="File not found")
        
        print(f"✅ Serving frontend from: {frontend_path}")
    else:
        print(f"⚠️ Frontend directory not found: {frontend_path}")
    
    # Initialize LLM provider (optional for fallback)
    llm_provider = None
    
    @app.on_event("startup")
    async def startup_event():
        global llm_provider
        try:
            print("Initializing LLM provider for RequirementRally...")
            llm_provider = get_llm_provider()
            print("✅ LLM provider initialized")
        except Exception as e:
            print(f"⚠️ LLM provider initialization failed: {e}")
            print("📋 Will use JSON database only (recommended for RequirementRally)")
            llm_provider = None
    
    # In-memory storage for RequirementRally sessions
    rally_sessions: Dict[str, Dict[str, Any]] = {}
    
    def cleanup_old_rally_sessions():
        """Remove sessions older than 1 hour"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_data in rally_sessions.items():
            session_created = datetime.fromisoformat(session_data["session"].created_at)
            if (current_time - session_created).total_seconds() > 3600:  # 1 hour
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del rally_sessions[session_id]
            print(f"🧹 Cleaned up expired RequirementRally session: {session_id}")
        
        return len(expired_sessions)
    
    async def generate_rally_scenarios(category: Optional[str] = None, difficulty: Optional[str] = None, count: int = 5, language: str = 'es') -> List[Dict[str, Any]]:
        """
        Generate scenarios for RequirementRally
        Primary: Use JSON database (reliable, fast)
        Fallback: Use LLM if needed (optional)
        """
        print(f"🎯 Generating {count} RequirementRally scenarios...")
        print(f"   Category filter: {category or 'mixed'}")
        print(f"   Difficulty filter: {difficulty or 'mixed'}")
        print(f"   Language: {language}")
        
        # Primary approach: Use JSON database
        try:
            scenarios = get_random_scenarios(count, category, difficulty, language)
            if scenarios and len(scenarios) >= count:
                print(f"✅ Successfully loaded {len(scenarios)} scenarios from JSON database")
                return scenarios
            else:
                print(f"⚠️ JSON database returned only {len(scenarios)} scenarios, need {count}")
        except Exception as e:
            print(f"❌ Error loading from JSON database: {e}")
        
        # Fallback approach: Use LLM if available
        if llm_provider:
            try:
                print("🤖 Falling back to LLM generation...")
                return await generate_llm_scenarios(category, difficulty, count, language)
            except Exception as e:
                print(f"❌ LLM generation failed: {e}")
        
        # Emergency fallback: Return empty with error
        print("❌ All scenario generation methods failed")
        return []

    async def generate_llm_scenarios(category: Optional[str], difficulty: Optional[str], count: int, language: str = 'es') -> List[Dict[str, Any]]:
        """Generate scenarios using LLM (fallback method)"""
        if not llm_provider:
            raise Exception("LLM provider not available")
        
        category_filter = f"focusing on {category} requirements" if category else "covering all requirement types"
        difficulty_filter = f"with {difficulty} difficulty level" if difficulty else "with mixed difficulty"
        
        lang_settings = {
            'es': {
                'prompt_suffix': 'en español',
                'options': ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
            },
            'en': {
                'prompt_suffix': 'in English',
                'options': ["Functional", "Non-Functional", "Constraint", "Not a requirement"]
            }
        }
        
        lang_config = lang_settings.get(language, lang_settings['es'])
        
        prompt = f"""Generate {count} different requirement identification scenarios for a software engineering education game {category_filter} {difficulty_filter} {lang_config['prompt_suffix']}.

Each scenario should test the ability to distinguish between:
1. Functional Requirements - What the system must DO (specific functions/features)
2. Non-Functional Requirements - HOW WELL the system must perform (quality attributes)
3. Constraints - Limitations or restrictions on the project/system

For each scenario, provide:
- A realistic requirement statement
- Four options: {', '.join([f'"{opt}"' for opt in lang_config['options']])}  
- The correct classification
- A clear explanation of why it belongs to that category

Format as JSON array with objects containing:
- id: unique identifier (req_XXX)
- content: the requirement statement in Spanish
- options: ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
- correctOption: "A", "B", "C", or "D"
- explanation: why this classification is correct
- category: "Functional", "Non-Functional", or "Constraint"
- difficulty: "easy", "medium", or "hard"

Return exactly {count} scenarios in valid JSON format."""
        
        try:
            response = await llm_provider.generate_async(prompt)
            # Parse LLM response (similar to QualityQuest parsing)
            scenarios = parse_llm_response(response)
            
            if len(scenarios) < count:
                print(f"⚠️ LLM generated only {len(scenarios)} scenarios, requested {count}")
            
            return scenarios
        
        except Exception as e:
            print(f"❌ LLM scenario generation failed: {e}")
            raise
    
    def parse_llm_response(response: str) -> List[Dict[str, Any]]:
        """Parse LLM response to extract scenarios"""
        try:
            # Try to find JSON in the response
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                # Try to find JSON object instead of array
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                
                if start_idx == -1 or end_idx == 0:
                    raise ValueError("No JSON found in LLM response")
            
            json_str = response[start_idx:end_idx]
            parsed = json.loads(json_str)
            
            # Ensure it's a list
            if isinstance(parsed, dict):
                parsed = [parsed]
            
            # Validate and standardize each scenario
            validated_scenarios = []
            for scenario in parsed:
                if validate_scenario_structure(scenario):
                    validated_scenarios.append(scenario)
            
            return validated_scenarios
            
        except Exception as e:
            print(f"❌ Failed to parse LLM response: {e}")
            return []
    
    def validate_scenario_structure(scenario: Dict[str, Any]) -> bool:
        """Validate that a scenario has the required structure"""
        required_fields = ['content', 'options', 'correctOption', 'explanation']
        return all(field in scenario for field in required_fields)
    
    # RequirementRally API endpoints
    
    @app.get("/")
    async def rally_root():
        return {"message": "RequirementRally Game Server", "status": "running", "game": "requirement-rally"}
    
    @app.get("/rally/stats")
    async def get_rally_stats():
        """Get RequirementRally database statistics"""
        try:
            stats = get_database_stats()
            validation = validate_scenarios()
            
            return {
                "database_stats": stats,
                "validation": validation,
                "server_info": {
                    "active_sessions": len(rally_sessions),
                    "llm_available": llm_provider is not None
                }
            }
        except Exception as e:
            print(f"❌ Error getting rally stats: {e}")
            raise HTTPException(status_code=500, detail="Failed to get statistics")
    
    @app.post("/rally/session")
    async def create_rally_session(request: RallySessionCreateRequest):
        """Create a new RequirementRally game session"""
        try:
            print(f"🎯 Creating RequirementRally session for: {request.name}")
            print(f"   Category: {request.category or 'mixed'}")
            print(f"   Difficulty: {request.difficulty or 'mixed'}")
            
            # Cleanup old sessions first
            cleanup_old_rally_sessions()
            
            # Generate scenarios
            scenarios = await generate_rally_scenarios(request.category, request.difficulty, 5, request.language)
            
            if not scenarios:
                raise HTTPException(status_code=500, detail="Failed to generate scenarios")
            
            # Create session
            session_id = str(uuid.uuid4())
            session = RallyGameSession(
                id=session_id,
                current_scenario=scenarios[0],
                created_at=datetime.now().isoformat(),
                category_filter=request.category,
                difficulty_filter=request.difficulty
            )
            
            # Store session data
            rally_sessions[session_id] = {
                "session": session,
                "scenarios": scenarios,
                "current_index": 0,
                "player_name": request.name
            }
            
            print(f"✅ Created RequirementRally session: {session_id[:8]}...")
            
            return {
                "session_id": session_id,
                "current_scenario": scenarios[0],
                "total_scenarios": len(scenarios),
                "game_info": {
                    "name": "RequirementRally",
                    "description": "Practice identifying requirement types",
                    "category_filter": request.category,
                    "difficulty_filter": request.difficulty
                }
            }
            
        except Exception as e:
            print(f"❌ Error creating RequirementRally session: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")
    
    @app.post("/rally/session/{session_id}/submit")
    async def submit_rally_answer(session_id: str, submission: RallyResponseSubmission):
        """Submit an answer for RequirementRally"""
        try:
            if session_id not in rally_sessions:
                raise HTTPException(status_code=404, detail="Session not found")
            
            session_data = rally_sessions[session_id]
            session = session_data["session"]
            scenarios = session_data["scenarios"]
            current_index = session_data["current_index"]
            
            if session.status != "active":
                raise HTTPException(status_code=400, detail="Session is not active")
            
            current_scenario = scenarios[current_index]
            correct_option = current_scenario["correctOption"]
            is_correct = submission.selected_option.upper() == correct_option.upper()
            
            # Update score and progress
            if is_correct:
                session.score += 10  # 10 points per correct answer
            
            session.scenarios_completed += 1
            
            # Check if game is completed
            game_completed = current_index >= len(scenarios) - 1
            next_scenario = None
            
            if not game_completed:
                session_data["current_index"] += 1
                next_scenario = scenarios[session_data["current_index"]]
                session.current_scenario = next_scenario
            else:
                session.status = "completed"
            
            print(f"🎯 RequirementRally answer submitted: {submission.selected_option} ({'✅' if is_correct else '❌'})")
            
            return RallyGameResponse(
                is_correct=is_correct,
                correct_answer=current_scenario["options"][ord(correct_option) - ord('A')],
                explanation=current_scenario["explanation"],
                score=session.score,
                next_scenario=next_scenario,
                game_completed=game_completed
            )
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error submitting RequirementRally answer: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")
    
    @app.get("/rally/session/{session_id}")
    async def get_rally_session(session_id: str):
        """Get RequirementRally session information"""
        try:
            if session_id not in rally_sessions:
                raise HTTPException(status_code=404, detail="Session not found")
            
            session_data = rally_sessions[session_id]
            session = session_data["session"]
            
            return {
                "session": session.dict(),
                "player_name": session_data["player_name"],
                "progress": {
                    "current": session_data["current_index"] + 1,
                    "total": len(session_data["scenarios"])
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error getting RequirementRally session: {e}")
            raise HTTPException(status_code=500, detail="Failed to get session")

except Exception as e:
    print(f"❌ Fatal error during RequirementRally server initialization: {e}")
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting RequirementRally server on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8002)