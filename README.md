# ISO Standards Games

An interactive educational application designed to teach ISO/IEC 25010, ISO/IEC/IEEE 29148, and ISO 9241 standards through gamification.

## Available Games

1. **QualityQuest**: Learn about the 8 quality attributes of ISO/IEC 25010
2. **ReqRally**: Understand requirements specification principles from ISO/IEC/IEEE 29148
3. **UXplorer**: Explore usability principles from ISO 9241
4. **StandardShowdown**: Integrate knowledge from all three standards
5. **QualityArchitect**: Apply standards in software design scenarios

## Features

- Interactive learning through gamification
- Progress tracking and scoring system
- Intelligent agents powered by LLM
- Bilingual support (English/Spanish)
- Detailed feedback and explanations

## Getting Started

### Prerequisites

- Python 3.9+
- Poetry package manager
- Ollama with gpt_oss model installed (or Azure OpenAI API access)

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd iso-standards-games
```

2. Install dependencies:
```
poetry install
```

3. Configure the application:
```
cp .env.example .env
```
Edit the `.env` file to configure your LLM provider (Ollama or Azure OpenAI).

### Running the application

```
poetry run python -m iso_standards_games
```

Access the web interface at http://localhost:8000

## Development

- Backend: FastAPI
- Frontend: ReactJS
- LLM Integration: Ollama (gpt_oss) / Azure OpenAI
- Testing: Pytest
- Localization: i18n

## License

This project is licensed under the MIT License - see the LICENSE file for details.