# HeatShield AI Docker Container
FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY tests/ ./tests/
COPY README.md LICENSE ./

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Run native standard library REST API server
CMD ["python3", "backend/server.py", "8000"]
