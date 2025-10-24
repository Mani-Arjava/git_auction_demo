# Dockerfile for Fly.io deployment
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Set Python path
ENV PYTHONPATH=/app

# Expose port (must match fly.toml internal_port)
EXPOSE 8080

# Run uvicorn server
CMD ["uvicorn", "app.api.server.app:app", "--host", "0.0.0.0", "--port", "8080"]
