#!/usr/bin/env python
"""Game server with LLM integration and scenarios database"""

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
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
    
    # Import LLM components
    from iso_standards_games.llm.provider import get_llm_provider
    from iso_standards_games.core.config import settings
    
    # Import the scenarios database
    from quality_scenarios_db import get_random_scenarios, get_database_stats
    
    # Import RequirementRally database
    from requirements_scenarios_db import get_random_scenarios as get_rally_scenarios, get_database_stats, validate_scenarios
    
    # Import UsabilityUniverse database
    from usability_scenarios_db import get_random_scenarios as get_usability_scenarios, get_database_stats as get_usability_stats, validate_scenarios as validate_usability_scenarios
    
    print("All modules imported successfully")
    
    # Pydantic models
    class SessionCreateRequest(BaseModel):
        name: str
        quality_attribute: str
        language: str = 'es'
    
    class GameSession(BaseModel):
        id: str
        game_id: str
        current_scenario: Dict[str, Any]
        status: str = "active"
        score: int = 0
        scenarios_completed: int = 0
        created_at: str
    
    class ResponseSubmission(BaseModel):
        selected_option: str
    
    # RequirementRally models
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
    
    # UsabilityUniverse models
    class UniverseSessionCreateRequest(BaseModel):
        name: str
        category: Optional[str] = None  # 'Learnability', 'Efficiency', 'Memorability', 'Error_Prevention', 'User_Satisfaction', or None for mixed
        difficulty: Optional[str] = None  # 'easy', 'medium', 'hard', or None for mixed
        language: str = 'en'  # Default to English
    
    class UniverseGameSession(BaseModel):
        id: str
        game_id: str = "usability-universe"
        current_scenario: Dict[str, Any]
        status: str = "active"
        score: int = 0
        scenarios_completed: int = 0
        created_at: str
        category_filter: Optional[str] = None
        difficulty_filter: Optional[str] = None
    
    class UniverseResponseSubmission(BaseModel):
        selected_option: str
    
    class UniverseGameResponse(BaseModel):
        is_correct: bool
        correct_answer: str
        explanation: str
        score: int
        next_scenario: Optional[Dict[str, Any]] = None
        game_completed: bool = False
    
    class GameResponse(BaseModel):
        is_correct: bool
        correct_answer: str
        explanation: str
        score: int
        next_scenario: Optional[Dict[str, Any]] = None
        game_completed: bool = False
    
    print("Creating app...")
    
    # Create FastAPI app
    app = FastAPI(title="ISO Standards Games API", version="1.0.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    

    
    # Initialize LLM provider
    llm_provider = None
    
    @app.on_event("startup")
    async def startup_event():
        global llm_provider
        try:
            print("Initializing LLM provider...")
            llm_provider = get_llm_provider()
            print("✅ LLM provider initialized")
        except Exception as e:
            print(f"⚠️ LLM provider initialization failed: {e}")
            llm_provider = None
    
    # In-memory storage for sessions with cleanup
    sessions: Dict[str, GameSession] = {}
    
    # In-memory storage for RequirementRally sessions
    rally_sessions: Dict[str, Dict[str, Any]] = {}
    
    # In-memory storage for UsabilityUniverse sessions
    universe_sessions: Dict[str, Dict[str, Any]] = {}
    
    def cleanup_old_sessions():
        """Remove sessions older than 1 hour"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_data in sessions.items():
            session_created = datetime.fromisoformat(session_data["session"].created_at)
            if (current_time - session_created).total_seconds() > 3600:  # 1 hour
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del sessions[session_id]
            print(f"🧹 Cleaned up expired session: {session_id}")
        
        return len(expired_sessions)
    
    def cleanup_old_rally_sessions():
        """Remove RequirementRally sessions older than 1 hour"""
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
    
    def cleanup_old_universe_sessions():
        """Remove UsabilityUniverse sessions older than 1 hour"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_data in universe_sessions.items():
            session_created = datetime.fromisoformat(session_data["session"].created_at)
            if (current_time - session_created).total_seconds() > 3600:  # 1 hour
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del universe_sessions[session_id]
            print(f"🧹 Cleaned up expired UsabilityUniverse session: {session_id}")
        
        return len(expired_sessions)
    
    async def generate_all_scenarios(quality_attribute: str = None, language: str = 'es') -> List[Dict[str, Any]]:
        """Generate all 5 scenarios at once using LLM or database fallback"""
        if not llm_provider:
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")
            print(f"⚠️ [{timestamp}] LLM not available, using database fallback")
            print(f"� [{timestamp}] CALLING get_random_scenarios() - should get NEW scenarios")
            
            scenarios = get_random_scenarios(5, quality_attribute, language, force_new_selection=True)
            
            print(f"🎲 [{timestamp}] RECEIVED from database:")
            for i, s in enumerate(scenarios):
                preview = s['content'][:40] + "..."
                print(f"   {i+1}. {s['id'][:8]}... - {preview}")
            
            return scenarios
        
        try:
            print(f"🤖 Generating all 5 scenarios with LLM for quality attribute: {quality_attribute or 'mixed'}...")
            
            # Create a prompt for generating all scenarios at once
            attribute_focus = f"with emphasis on {quality_attribute}" if quality_attribute else "covering different quality attributes"
            prompt = f"""Generate 5 different software quality scenarios for the ISO/IEC 25010 quality model learning game {attribute_focus}.
            
Each scenario should test understanding of one of these quality characteristics:
1. Functional Suitability - Does the software provide functions that meet stated needs?
2. Performance Efficiency - How well does the software perform relative to resources used?
3. Compatibility - Can the software coexist and exchange information with other systems?
4. Usability - How easy is it for users to achieve their goals?
5. Reliability - Does the software maintain specified performance under stated conditions?
6. Security - Does the software protect information and data?
7. Maintainability - How easy is it to modify the software?
8. Portability - How easy is it to transfer the software to different environments?

For each scenario, provide:
- A realistic business/technical situation
- The correct quality characteristic (from the 8 above)
- A clear explanation of why this characteristic applies

Format your response as a JSON array with objects containing:
- content: the scenario description
- correctOption: "A", "B", "C", or "D" 
- explanation: why this quality characteristic applies
- qualityAttribute: the specific quality characteristic name

Return exactly 5 scenarios in JSON format."""
            
            # Add timeout to LLM call to prevent hanging
            response = await asyncio.wait_for(
                llm_provider.generate_structured_output(prompt, {}),
                timeout=15.0  # 15 seconds timeout
            )
            
            # Handle LLM response parsing
            scenarios_data = None
            
            if isinstance(response, dict) and 'scenarios' in response:
                scenarios_data = response['scenarios']
            elif isinstance(response, list):
                scenarios_data = response
            elif isinstance(response, dict) and 'error' in response and 'text' in response:
                # Handle JSON wrapped in markdown code blocks
                text = response['text']
                print(f"🔧 Attempting to parse JSON from markdown-wrapped response")
                
                # Extract JSON from markdown code blocks
                import re
                json_match = re.search(r'```json\s*\n(.*?)\n```', text, re.DOTALL)
                if json_match:
                    try:
                        import json
                        json_text = json_match.group(1)
                        scenarios_data = json.loads(json_text)
                        print(f"✅ Successfully parsed {len(scenarios_data)} scenarios from markdown JSON")
                    except json.JSONDecodeError as e:
                        print(f"❌ Failed to parse extracted JSON: {e}")
                        scenarios_data = None
                else:
                    print(f"❌ No JSON block found in response")
            
            if scenarios_data is None:
                print(f"⚠️ Unexpected response format: {response}")
                return get_random_scenarios(5, quality_attribute, language)
            
            # Standard quality attributes for options generation
            QUALITY_ATTRIBUTES = {
                "es": ["Aptitud Funcional", "Eficiencia de desempeño", "Compatibilidad", "Usabilidad", "Fiabilidad", "Seguridad", "Mantenibilidad", "Portabilidad"],
                "en": ["Functional Suitability", "Performance Efficiency", "Compatibility", "Usability", "Reliability", "Security", "Maintainability", "Portability"]
            }
            
            scenarios = []
            for i, scenario_data in enumerate(scenarios_data[:5]):
                if isinstance(scenario_data, dict):
                    # Get quality attribute and normalize it
                    quality_attr = scenario_data.get('qualityAttribute', 'Unknown')
                    correct_option = scenario_data.get('correctOption', 'A')
                    
                    # Generate options with the correct answer in the right position
                    attributes_list = QUALITY_ATTRIBUTES[language]
                    
                    # Try to find the quality attribute in our standard list
                    correct_attr = quality_attr
                    for std_attr in attributes_list:
                        if quality_attr.lower().replace(' ', '') in std_attr.lower().replace(' ', ''):
                            correct_attr = std_attr
                            break
                    
                    # Create options with correct answer in specified position
                    import random
                    other_attrs = [attr for attr in attributes_list if attr != correct_attr]
                    random.shuffle(other_attrs)
                    
                    options = {}
                    option_keys = ['A', 'B', 'C', 'D']
                    
                    # Place correct answer in the specified position
                    correct_index = ord(correct_option) - ord('A')
                    if correct_index < 0 or correct_index >= 4:
                        correct_index = 0  # Default to A if invalid
                    
                    # Fill options
                    for j, key in enumerate(option_keys):
                        if j == correct_index:
                            options[key] = correct_attr
                        else:
                            # Use other attributes, cycling if needed
                            attr_index = (j - (1 if j > correct_index else 0)) % len(other_attrs)
                            options[key] = other_attrs[attr_index]
                    
                    scenario = {
                        "id": str(uuid.uuid4()),
                        "content": scenario_data.get('content', f'Generated scenario {i+1}'),
                        "options": options,
                        "correctOption": correct_option,
                        "explanation": scenario_data.get('explanation', 'LLM-generated explanation'),
                        "category": correct_attr
                    }
                    scenarios.append(scenario)
            
            print(f"✅ Generated {len(scenarios)} scenarios with LLM")
            
            # Fill with database scenarios if we don't have enough
            while len(scenarios) < 5:
                needed = 5 - len(scenarios)
                fallback_scenarios = get_random_scenarios(needed, quality_attribute, language)
                print(f"🎲 Adding {len(fallback_scenarios)} database scenarios: {[s['id'][:8] + '...' for s in fallback_scenarios]}")
                scenarios.extend(fallback_scenarios)
            
            return scenarios[:5]
                
        except asyncio.TimeoutError:
            print("⏰ LLM timeout (15s) - using database fallback for faster response")
            fallback_scenarios = get_random_scenarios(5, quality_attribute, language)
            print(f"🎲 Using database fallback: {[s['id'][:8] + '...' for s in fallback_scenarios]}")
            print(f"🔍 First fallback scenario: {fallback_scenarios[0]['content'][:50]}...")
            return fallback_scenarios
        except Exception as e:
            print(f"❌ Error generating scenarios with LLM: {e}")
            fallback_scenarios = get_random_scenarios(5, quality_attribute, language)
            print(f"🎲 Using database fallback: {[s['id'][:8] + '...' for s in fallback_scenarios]}")
            print(f"🔍 First fallback scenario: {fallback_scenarios[0]['content'][:50]}...")
            return fallback_scenarios
    
    # RequirementRally helper functions
    async def generate_rally_scenarios(category: Optional[str] = None, difficulty: Optional[str] = None, count: int = 5, language: str = 'es') -> List[Dict[str, Any]]:
        """Generate scenarios for RequirementRally"""
        print(f"🎯 Generating {count} RequirementRally scenarios...")
        print(f"   Category filter: {category or 'mixed'}")
        print(f"   Difficulty filter: {difficulty or 'mixed'}")
        print(f"   Language: {language}")
        
        try:
            scenarios = get_rally_scenarios(count, category, difficulty, language)
            if scenarios and len(scenarios) >= count:
                print(f"✅ Successfully loaded {len(scenarios)} scenarios from RequirementRally database")
                return scenarios
            else:
                print(f"⚠️ RequirementRally database returned only {len(scenarios) if scenarios else 0} scenarios, need {count}")
                return scenarios or []
        except Exception as e:
            print(f"❌ Error loading from RequirementRally database: {e}")
            return []
    
    def validate_rally_scenario_structure(scenario: Dict[str, Any]) -> bool:
        """Validate that a RequirementRally scenario has the required structure"""
        required_fields = ['content', 'options', 'correctOption', 'explanation']
        return all(field in scenario for field in required_fields)
    
    # Add route to serve frontend
    from fastapi.responses import FileResponse
    
    @app.get("/")
    async def serve_frontend():
        frontend_index = os.path.join(os.path.dirname(__file__), "iso_standards_games", "frontend", "dist", "index.html")
        if os.path.exists(frontend_index):
            return FileResponse(frontend_index)
        else:
            return {
                "message": "ISO Standards Games API with LLM and Scenarios Database", 
                "version": "2.0.0",
                "llm_available": llm_provider is not None,
                "database_stats": get_database_stats()
            }
    
    @app.get("/api/v1/games/")
    async def list_games():
        """List available games"""
        db_stats = get_database_stats()
        return {
            "games": [
                {
                    "id": "quality_quest",
                    "name": "Quality Quest",
                    "description": "Learn ISO/IEC 25010 software quality characteristics",
                    "difficulty": 1,
                    "llm_enabled": llm_provider is not None,
                    "scenario_database": {
                        "total_scenarios": db_stats.get("total", 0),
                        "quality_attributes": len(db_stats.get("attributes", {})),
                        "scenarios_per_attribute": db_stats.get("by_attribute", {})
                    }
                }
            ]
        }
    
    @app.post("/api/v1/games/{game_id}/sessions")
    async def create_game_session(game_id: str, language: str = 'es'):
        """Create a new game session with all scenarios pre-generated"""
        # Clean up old sessions first
        cleanup_old_sessions()
        
        session_id = str(uuid.uuid4())
        
        print(f"📝 Creating new session for {game_id} (Session ID: {session_id[:8]})")
        
        # Generate ALL scenarios at once using LLM or database - FRESH for each session
        all_scenarios = await generate_all_scenarios(language=language)
        print(f"🎲 Generated {len(all_scenarios)} fresh scenarios for session {session_id[:8]}")
        
        session = GameSession(
            id=session_id,
            game_id=game_id,
            current_scenario=all_scenarios[0],  # First scenario
            created_at=datetime.now().isoformat()
        )
        
        # Store all scenarios in session
        sessions[session_id] = {
            "session": session,
            "all_scenarios": all_scenarios,
            "current_index": 0
        }
        
        print(f"✅ Session created with ID: {session_id}")
        
        return {
            "id": session_id,  # Frontend expects 'id', not 'session_id'
            "session_id": session_id,  # Keep both for compatibility
            "current_scenario": all_scenarios[0],  # Frontend expects 'current_scenario'
            "scenario": all_scenarios[0],  # Keep both for compatibility
            "message": "Session created successfully with pre-generated scenarios"
        }
    
    @app.post("/api/v1/games/{game_id}/sessions/{session_id}/response")
    async def submit_response(game_id: str, session_id: str, response: ResponseSubmission):
        """Submit a response and get next pre-generated scenario"""
        
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        session = session_data["session"]
        all_scenarios = session_data["all_scenarios"]
        current_index = session_data["current_index"]
        
        current_scenario = all_scenarios[current_index]
        
        print(f"📥 Processing response for session {session_id} (scenario {current_index + 1}/5)")
        
        # Check if answer is correct
        is_correct = response.selected_option == current_scenario.get("correctOption", "A")
        
        # Update score
        if is_correct:
            session.score += 10
            print(f"✅ Correct answer! Score: {session.score}")
        else:
            print(f"❌ Incorrect answer. Score remains: {session.score}")
        
        session.scenarios_completed += 1
        
        # Determine next scenario
        next_index = current_index + 1
        next_scenario = None
        game_completed = False
        
        if next_index < len(all_scenarios):
            next_scenario = all_scenarios[next_index]
            session.current_scenario = next_scenario
            sessions[session_id]["current_index"] = next_index
            print(f"📋 Moving to scenario {next_index + 1}/5")
        else:
            game_completed = True
            session.status = "completed"
            print(f"🎉 Game completed! Final score: {session.score}")
        
        return GameResponse(
            is_correct=is_correct,
            correct_answer=current_scenario.get("correctOption", "A"),
            explanation=current_scenario.get("explanation", "Demo explanation"),
            score=session.score,
            next_scenario=next_scenario,
            game_completed=game_completed
        )
    
    @app.get("/api/v1/games/{game_id}/sessions/{session_id}")
    async def get_session(game_id: str, session_id: str):
        """Get session details"""
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[session_id]
        return session_data["session"]
    
    # Endpoint compatible with frontend
    @app.post("/api/create-session")
    async def create_session(request: SessionCreateRequest):
        """Create a new session (compatible with frontend)"""
        print(f"🎯 RECEIVED /api/create-session request: name={request.name}, quality={request.quality_attribute}, language={request.language}")
        
        # Clean up old sessions first
        cleanup_old_sessions()
        
        session_id = str(uuid.uuid4())
        
        print(f"📝 Creating new session for user: {request.name}, quality: {request.quality_attribute} (Session ID: {session_id[:8]})")
        
        # Generate ALL scenarios at once using LLM with focus on quality attribute 
        all_scenarios = await generate_all_scenarios(request.quality_attribute, request.language)
        
        session = GameSession(
            id=session_id,
            game_id="quality_quest",
            current_scenario=all_scenarios[0],  # First scenario
            created_at=datetime.now().isoformat()
        )
        
        # Store all scenarios in session
        sessions[session_id] = {
            "session": session,
            "all_scenarios": all_scenarios,
            "current_index": 0
        }
        
        print(f"✅ Session created with ID: {session_id}")
        
        return {
            "id": session_id,  # Frontend expects 'id'
            "session_id": session_id,
            "game_id": "quality_quest", 
            "current_scenario": all_scenarios[0],  # Frontend expects 'current_scenario'
            "scenario": all_scenarios[0],
            "message": f"Welcome {request.name}! Starting with scenario 1 of 5 from quality database."
        }
    
    # RequirementRally API endpoints
    
    @app.get("/rally/stats")
    async def get_rally_stats():
        """Get RequirementRally database statistics"""
        try:
            print("🔍 Starting rally stats endpoint...")
            
            # Return only a simple static response first
            return {
                "status": "working",
                "message": "Rally stats endpoint is functional"
            }
            
        except Exception as e:
            print(f"❌ Error getting rally stats: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")
    
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
    
    # Mount RequirementRally frontend 
    rally_frontend_path = os.path.join(os.path.dirname(__file__), "requirement-rally-frontend")
    if os.path.exists(rally_frontend_path):
        @app.get("/requirement-rally")
        async def serve_rally_frontend():
            print(f"🔄 Serving RequirementRally frontend: {rally_frontend_path}/index.html")
            return FileResponse(os.path.join(rally_frontend_path, "index.html"))
            
        @app.get("/requirement-rally/{file_path:path}")
        async def serve_rally_static(file_path: str):
            print(f"🔄 Serving RequirementRally static file: {file_path}")
            if file_path.startswith("rally/"):  # Don't serve API routes as static files
                print(f"❌ Blocked API route: {file_path}")
                raise HTTPException(status_code=404, detail="Not found")
            
            file_location = os.path.join(rally_frontend_path, file_path)
            print(f"🔍 Looking for file at: {file_location}")
            if os.path.exists(file_location) and os.path.isfile(file_location):
                print(f"✅ Found file: {file_location}")
                return FileResponse(file_location)
            print(f"❌ File not found: {file_location}")
            raise HTTPException(status_code=404, detail="File not found")
        
        print(f"✅ Mounted RequirementRally frontend from: {rally_frontend_path}")
    else:
        print(f"⚠️ RequirementRally frontend directory not found: {rally_frontend_path}")
    
    # ========== USABILITYUNIVERSE ENDPOINTS ==========
    
    @app.post("/universe/session")
    async def create_universe_session(request: UniverseSessionCreateRequest):
        """Create a new UsabilityUniverse game session"""
        try:
            print(f"🚀 Creating UsabilityUniverse session for player: {request.name}")
            print(f"   Category: {request.category}, Difficulty: {request.difficulty}, Language: {request.language}")
            
            # Cleanup old sessions periodically
            cleanup_old_universe_sessions()
            
            # Generate session ID
            session_id = str(uuid.uuid4())
            
            # Get scenarios from database with improved variety
            scenarios = get_usability_scenarios(
                count=5,
                category=request.category,
                difficulty=request.difficulty,
                language=request.language,
                force_new_selection=True
            )
            
            if not scenarios:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No scenarios found for category: {request.category}, difficulty: {request.difficulty}"
                )
            
            # Create session object
            session = UniverseGameSession(
                id=session_id,
                current_scenario=scenarios[0],
                created_at=datetime.now().isoformat(),
                category_filter=request.category,
                difficulty_filter=request.difficulty
            )
            
            # Store session data
            universe_sessions[session_id] = {
                "session": session,
                "scenarios": scenarios,
                "current_index": 0,
                "player_name": request.name,
                "language": request.language
            }
            
            print(f"✅ UsabilityUniverse session created: {session_id} with {len(scenarios)} scenarios")
            return session
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error creating UsabilityUniverse session: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")
    
    @app.post("/universe/session/{session_id}/submit")
    async def submit_universe_answer(session_id: str, submission: UniverseResponseSubmission):
        """Submit an answer for a UsabilityUniverse scenario"""
        try:
            print(f"📝 UsabilityUniverse answer submitted for session: {session_id}")
            print(f"   Selected option: {submission.selected_option}")
            
            if session_id not in universe_sessions:
                raise HTTPException(status_code=404, detail="Session not found")
            
            session_data = universe_sessions[session_id]
            session = session_data["session"]
            scenarios = session_data["scenarios"]
            current_index = session_data["current_index"]
            
            if current_index >= len(scenarios):
                raise HTTPException(status_code=400, detail="No more scenarios available")
            
            current_scenario = scenarios[current_index]
            correct_answer = current_scenario["correct_answer"]
            
            # Evaluate answer
            is_correct = submission.selected_option.lower() == correct_answer.lower()
            
            # Update score
            if is_correct:
                session.score += 10
            
            session.scenarios_completed += 1
            
            # Move to next scenario
            session_data["current_index"] += 1
            next_scenario = None
            game_completed = session_data["current_index"] >= len(scenarios)
            
            if not game_completed:
                next_scenario = scenarios[session_data["current_index"]]
                session.current_scenario = next_scenario
            else:
                session.status = "completed"
            
            print(f"✅ Answer evaluated: {'Correct' if is_correct else 'Incorrect'}")
            print(f"   Score: {session.score}, Completed: {session.scenarios_completed}/{len(scenarios)}")
            
            return UniverseGameResponse(
                is_correct=is_correct,
                correct_answer=correct_answer,
                explanation=current_scenario.get("feedback", "No explanation available"),
                score=session.score,
                next_scenario=next_scenario,
                game_completed=game_completed
            )
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Error submitting UsabilityUniverse answer: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")
    
    @app.get("/universe/session/{session_id}")
    async def get_universe_session(session_id: str):
        """Get UsabilityUniverse session information"""
        try:
            if session_id not in universe_sessions:
                raise HTTPException(status_code=404, detail="Session not found")
            
            session_data = universe_sessions[session_id]
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
            print(f"❌ Error getting UsabilityUniverse session: {e}")
            raise HTTPException(status_code=500, detail="Failed to get session")
    
    # Mount UsabilityUniverse frontend 
    universe_frontend_path = os.path.join(os.path.dirname(__file__), "usability-universe-frontend")
    if os.path.exists(universe_frontend_path):
        @app.get("/usability-universe")
        async def serve_universe_frontend():
            print(f"🔄 Serving UsabilityUniverse frontend: {universe_frontend_path}/index.html")
            return FileResponse(os.path.join(universe_frontend_path, "index.html"))
            
        @app.get("/usability-universe/{file_path:path}")
        async def serve_universe_static(file_path: str):
            print(f"🔄 Serving UsabilityUniverse static file: {file_path}")
            if file_path.startswith("universe/"):  # Don't serve API routes as static files
                print(f"❌ Blocked API route: {file_path}")
                raise HTTPException(status_code=404, detail="Not found")
            
            file_location = os.path.join(universe_frontend_path, file_path)
            print(f"🔍 Looking for file at: {file_location}")
            if os.path.exists(file_location) and os.path.isfile(file_location):
                print(f"✅ Found file: {file_location}")
                return FileResponse(file_location)
            print(f"❌ File not found: {file_location}")
            raise HTTPException(status_code=404, detail="File not found")
        
        print(f"✅ Mounted UsabilityUniverse frontend from: {universe_frontend_path}")
        
        # Special route for UsabilityUniverse JavaScript file (needed by main frontend)
        @app.get("/usability-universe.js")
        async def serve_universe_js():
            js_file = os.path.join(universe_frontend_path, "usability-universe.js")
            print(f"🔄 Serving UsabilityUniverse JS for main frontend: {js_file}")
            if os.path.exists(js_file):
                return FileResponse(js_file, media_type="application/javascript")
            else:
                print(f"❌ UsabilityUniverse JS not found: {js_file}")
                raise HTTPException(status_code=404, detail="JavaScript file not found")
                
    else:
        print(f"⚠️ UsabilityUniverse frontend directory not found: {universe_frontend_path}")
    
    # Mount static files AFTER all API routes are defined
    frontend_dist = os.path.join(os.path.dirname(__file__), "iso_standards_games", "frontend", "dist")
    if os.path.exists(frontend_dist):
        # Mount assets directory
        app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
        # Mount games directory  
        app.mount("/games", StaticFiles(directory=os.path.join(frontend_dist, "games"), html=True), name="games")
        print(f"✅ Mounted frontend from: {frontend_dist}")
    else:
        print(f"⚠️ Frontend dist directory not found: {frontend_dist}")
    
    # Serve configuration file
    @app.get("/config.js")
    async def serve_config():
        config_path = os.path.join(os.path.dirname(__file__), "config.js")
        if os.path.exists(config_path):
            return FileResponse(config_path, media_type="application/javascript")
        else:
            return {"error": "Configuration file not found"}
    
    print("App created successfully with LLM integration and scenarios database")
    
    # Only run server if this script is executed directly
    if __name__ == "__main__":
        print("Importing uvicorn...")
        import uvicorn
        print("Uvicorn imported successfully")
        
        print("Starting server on port 8001...")
        uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")

except Exception as e:
    print(f"❌ Error during startup: {e}")
    traceback.print_exc()
    sys.exit(1)