# ==============================================================================
# 🐾 Evcil Hayvan Platformu - Multi-Stage Docker Build
# ==============================================================================
# Production-ready, secure, optimized Django container
# ==============================================================================

# ==============================================================================
# 🔧 BUILD STAGE - Dependencies ve static files
# ==============================================================================
FROM python:3.12-slim-bookworm as builder

# Build arguments
ARG ENVIRONMENT=production
ARG POETRY_VERSION=1.7.1

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# Install system dependencies with security updates
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    libpq-dev \
    libmagic1 \
    curl \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Create app directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# ==============================================================================
# 🚀 PRODUCTION STAGE - Optimized runtime
# ==============================================================================
FROM python:3.12-slim-bookworm as production

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.settings.production

# Install runtime dependencies with security updates
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    libpq5 \
    libmagic1 \
    curl \
    ca-certificates \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Create app directory and set permissions
RUN mkdir -p /app /app/staticfiles /app/media /app/logs \
    && chown -R appuser:appgroup /app

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appgroup /app/venv /app/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput --settings=config.settings.production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Expose port
EXPOSE 8000

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--worker-class", "gevent", "config.wsgi:application"]

# ==============================================================================
# 🛠️ DEVELOPMENT STAGE - Hot reload ve debugging
# ==============================================================================
FROM python:3.12-slim-bookworm as development

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.settings.development

# Install system dependencies with security updates
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    libpq-dev \
    libmagic1 \
    build-essential \
    curl \
    git \
    vim \
    ca-certificates \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -s /bin/bash appuser

# Create app directory
RUN mkdir -p /app && chown -R appuser:appgroup /app

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
RUN pip install --no-cache-dir \
    ipython \
    django-debug-toolbar \
    django-extensions \
    pytest \
    pytest-django \
    factory-boy

# Switch to non-root user
USER appuser

# Development command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
