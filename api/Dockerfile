FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git

# Copy the requirements file and install dependencies
COPY ./pyproject.toml ./requirements.txt /app/

# Change directory to where your FastAPI application code is located
WORKDIR /app/src

# Copy the application code from the api/src/ directory
COPY ./src/ ./

WORKDIR /app

RUN pip install --no-cache-dir -e .

# Expose the port on which the FastAPI application will run
EXPOSE 8000

# Define the command to start the FastAPI application
CMD ["uvicorn", "llamp.main:app", "--host", "0.0.0.0", "--port", "8000"]

