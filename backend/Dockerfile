# Use official Python image as base
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy application files
COPY . /app

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app

# Install dependencies
RUN apt-get update
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn openai google-auth google-auth-oauthlib sqlalchemy alembic psycopg2-binary dotenv google-auth-httplib2 google-api-python-client pyjwt

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
