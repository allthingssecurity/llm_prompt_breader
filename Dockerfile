# Dockerfile for LLM-Picbreeder
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Environment variables
ENV OPENAI_API_KEY=\"\"
ENV DATABASE_URL=\"sqlite:///./llm_picbreeder.db\"

# Run the application
CMD [\"uvicorn\", \"llm_picbreeder.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]