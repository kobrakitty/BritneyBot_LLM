#!/bin/bash

# Print system information
echo "Current PATH: $PATH"
echo "Current working directory: $(pwd)"
echo "Operating System: $(uname -a)"

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing..."
    curl https://ollama.ai/install.sh | sh
    export PATH=$PATH:/usr/local/bin
    echo "Updated PATH: $PATH"
fi

# Pull the llama3 model
ollama pull llama3:8b

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port $PORT