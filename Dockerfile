# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 10000 available to the world outside this container
EXPOSE 10000

# Set the environment variable for the Ollama URL
ENV OLLAMA_URL=https://6bea-2600-1700-f7c1-14d0-49c-8e7f-81c3-fbb2.ngrok-free.app/

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]