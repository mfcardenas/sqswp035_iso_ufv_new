"""Main module for ISO Standards Games application."""

import uvicorn

from iso_standards_games.api.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "iso_standards_games.__main__:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )