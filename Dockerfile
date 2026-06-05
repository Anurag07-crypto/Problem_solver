FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy project files
COPY . .

EXPOSE 8000

CMD ["uv", "run", "streamlit", "run", "Frontend/Home.py", "--server.address=0.0.0.0", "--server.port=8000"]