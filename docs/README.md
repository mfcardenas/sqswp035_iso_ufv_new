# ISO Standards Games Documentation

## Overview

ISO Standards Games is an educational application designed to help students learn about ISO/IEC 25010, ISO/IEC/IEEE 29148, and ISO 9241 standards through interactive gamification. The application features multiple games with increasing complexity, designed to teach students the "why" and "what" of these standards before applying them in depth.

## Architecture

The application is built with a modern architecture:

- **Backend**: FastAPI (Python)
- **Frontend**: React with TypeScript
- **LLM Integration**: Ollama (gpt_oss) and/or Azure OpenAI
- **Agent System**: Autonomous agents for scenario generation and evaluation
- **Internationalization**: Support for English and Spanish

## Game Descriptions

1. **QualityQuest**: Introduction to ISO/IEC 25010 quality attributes
2. **ReqRally**: Learning ISO/IEC/IEEE 29148 requirements specification
3. **UXplorer**: Exploring ISO 9241 usability principles
4. **StandardShowdown**: Integration of all standards
5. **QualityArchitect**: Application of standards in software design

## Directory Structure

```
iso-standards-games/
├── iso_standards_games/             # Main package
│   ├── __init__.py
│   ├── __main__.py                  # Entry point
│   ├── api/                         # API endpoints
│   │   ├── __init__.py
│   │   ├── app.py                   # FastAPI application
│   │   ├── routes.py                # Main router
│   │   └── v1/                      # API version 1
│   │       ├── games.py             # Game endpoints
│   │       └── users.py             # User endpoints
│   ├── core/                        # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                # Settings
│   │   ├── localization.py          # i18n utilities
│   │   └── models.py                # Data models
│   ├── llm/                         # LLM integration
│   │   ├── __init__.py
│   │   └── provider.py              # LLM providers
│   ├── agents/                      # Intelligent agents
│   │   ├── __init__.py
│   │   ├── base.py                  # Base agent class
│   │   └── game_agents.py           # Game-specific agents
│   ├── games/                       # Game implementations
│   │   ├── __init__.py
│   │   ├── base.py                  # Base game class
│   │   ├── manager.py               # Game manager
│   │   ├── quality_quest.py         # QualityQuest implementation
│   │   └── ... (other games)
│   ├── locales/                     # Translations
│   │   ├── en/
│   │   │   └── translation.json
│   │   └── es/
│   │       └── translation.json
│   └── frontend/                    # React frontend
│       ├── public/
│       ├── src/
│       └── ... (frontend files)
├── tests/                           # Test suite
├── pyproject.toml                   # Poetry configuration
├── .env.example                     # Environment variables example
└── README.md                        # Project readme
```

## API Documentation

### Games API

#### GET `/api/v1/games/`

List all available games.

**Response**:
```json
{
  "games": [
    {
      "id": "quality_quest",
      "name": "QualityQuest: The Quality Challenge",
      "description": "...",
      "difficulty": 1,
      "tags": ["ISO 25010", "Quality", "Beginner"]
    },
    ...
  ]
}
```

#### GET `/api/v1/games/{game_id}`

Get detailed information about a specific game.

**Response**:
```json
{
  "id": "quality_quest",
  "name": "QualityQuest: The Quality Challenge",
  "description": "...",
  "difficulty": 1,
  "tags": ["ISO 25010", "Quality", "Beginner"],
  "objectives": ["..."],
  "standards_covered": ["ISO/IEC 25010"],
  "estimated_duration_minutes": 20
}
```

#### POST `/api/v1/games/{game_id}/sessions`

Start a new game session.

**Response**:
```json
{
  "id": "session_uuid",
  "game_id": "quality_quest",
  "current_scenario": {
    "id": "scenario_id",
    "content": "...",
    "options": [
      {"id": "A", "text": "Option A"},
      ...
    ],
    "type": "multiple_choice"
  },
  "score": 0,
  "started_at": "2023-09-27T14:30:00",
  "completed": false
}
```

#### POST `/api/v1/games/{game_id}/sessions/{session_id}/response`

Submit a response to a game scenario.

**Request**:
```json
{
  "selected_option_id": "A"
}
```

**Response**:
```json
{
  "correct": true,
  "explanation": "That's correct! Functional Suitability...",
  "points_earned": 10,
  "next_scenario": {...},
  "game_completed": false,
  "feedback": "Additional learning point..."
}
```

## LLM Integration

The application can use either Ollama's gpt_oss model or Azure OpenAI. The LLM is used to:

1. Generate realistic scenarios based on ISO standards
2. Evaluate user responses and provide educational feedback
3. Adapt difficulty based on user performance
4. Create personalized learning paths

## Frontend Design

The frontend is designed with a modern, engaging interface:

- Responsive design for all devices
- Interactive game elements
- Progress tracking and badges
- Real-time feedback
- Language switching between English and Spanish
- Accessibility features

## Setup and Configuration

1. Install dependencies:
```
poetry install
```

2. Set up environment variables:
```
cp .env.example .env
```

3. Edit `.env` to configure your preferred LLM provider.

4. Run the application:
```
poetry run python -m iso_standards_games
```

## Testing

Run the test suite:
```
poetry run pytest
```