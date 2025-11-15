# ============================================
# Dockerfile for ISO Standards Games
# ============================================
# Multi-stage build for optimized image size
# Deploys FastAPI server on port 8001
# Includes all three games: QualityQuest, RequirementRally, UsabilityUniverse
# ============================================

# ============================================
# Stage 1: Builder - Install dependencies
# ============================================
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy Poetry configuration files
COPY pyproject.toml ./

# Configure Poetry to not create virtual environment (we're in a container)
RUN poetry config virtualenvs.create false

# Install Python dependencies (without development dependencies)
RUN poetry install --only main --no-interaction --no-ansi

# Export dependencies to requirements.txt for future use if needed
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only main

# ============================================
# Stage 2: Runtime - Create final image
# ============================================
FROM python:3.9-slim as runtime

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy entire project structure
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_NAME="ISO Standards Games" \
    DEBUG=false \
    DEFAULT_LOCALE=en \
    LLM_PROVIDER=ollama \
    OLLAMA_BASE_URL=http://localhost:11434 \
    OLLAMA_MODEL=qwen3 \
    DATABASE_URL=sqlite:///./iso_standards_games.db

# Expose port 8001
EXPOSE 8001

# Health check to verify the server is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/').read()" || exit 1

# Run the FastAPI server
# Using uvicorn directly with host 0.0.0.0 to accept connections from outside container
# Port 8001 as specified in the requirements
CMD ["python", "-m", "uvicorn", "llm_game_server:app", "--host", "0.0.0.0", "--port", "8001"]
