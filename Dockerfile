FROM python:3.11-slim

# Install system dependencies first (these cache well)
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

# Copy dependency files first - these change infrequently
COPY pyproject.toml uv.lock ./

# Install dependencies with better caching
# Use --frozen to ensure reproducible builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --compile-bytecode 2>&1 | tee /tmp/install.log || \
    (tail -50 /tmp/install.log && exit 1)

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p logs database && \
    chmod +x entrypoint.sh

# Expose ports: 8000 for FastAPI, 8501 for Streamlit
EXPOSE 8000 8501

# Health check for backend
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Run startup script
CMD ["./entrypoint.sh"]