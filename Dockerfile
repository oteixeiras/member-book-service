# Use Python 3.9 slim to match project
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (pinned versions)
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    "uvicorn[standard]"==0.24.0 \
    sqlalchemy==2.0.23 \
    alembic==1.12.1 \
    psycopg2-binary==2.9.9 \
    python-multipart==0.0.6 \
    pydantic==2.5.0 \
    pydantic-settings==2.1.0 \
    gunicorn==21.2.0

# Copy application code
COPY . .

# Entrypoint script
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default runtime envs
ENV LOG_LEVEL=info \
    WORKERS=2 \
    TIMEOUT=60 \
    ENVIRONMENT=production

# Run the application via entrypoint (runs migrations then server)
ENTRYPOINT ["/app/docker-entrypoint.sh"]
