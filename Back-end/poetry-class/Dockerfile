# Use an official Python runtime as a parent image
FROM python:3.12

LABEL maintainer="sarmad426"

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy the Poetry files from the root directory
COPY pyproject.toml poetry.lock /app/

# Configuration to avoid creating virtual environments inside the Docker container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install

# Copy the entire project into the container
COPY . /app/

# Set PYTHONPATH to include the poetryclass directory
ENV PYTHONPATH=/app/poetryclass

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the app. CMD can be overridden when starting the container
CMD ["poetry", "run", "uvicorn", "poetryclass.todo_app.main:app", "--host", "0.0.0.0", "--reload"]
