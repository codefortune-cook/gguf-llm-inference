#!/bin/bash

# GGUF LLM Inference - Docker Run Examples
# This script provides example commands for running the dockerized inference

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check if model directory exists
if [ ! -d "./models" ]; then
    print_warning "Models directory not found. Creating it..."
    mkdir -p models
fi

# Check if any .gguf files exist
if [ -z "$(find ./models -name "*.gguf" 2>/dev/null)" ]; then
    print_warning "No GGUF model files found in ./models/"
    print_status "Please place your GGUF model files in the ./models/ directory"
    echo "Example:"
    echo "  mkdir -p models"
    echo "  # Download or copy your .gguf model file to models/"
    echo ""
fi

# Build the image if it doesn't exist
if [ -z "$(docker images -q gguf-inference 2>/dev/null)" ]; then
    print_header "Building Docker Image"
    docker build -t gguf-inference .
    print_status "Docker image built successfully!"
fi

# Function to get first available model
get_model_path() {
    local model_file=$(find ./models -name "*.gguf" | head -1)
    if [ -n "$model_file" ]; then
        echo "/app/models/$(basename "$model_file")"
    else
        echo "/app/models/your-model.gguf"
    fi
}

MODEL_PATH=$(get_model_path)

print_header "Available Commands"

echo "1. Interactive Mode"
echo "   docker run -it --rm \\"
echo "     -v \$(pwd)/models:/app/models:ro \\"
echo "     -v \$(pwd)/outputs:/app/outputs \\"
echo "     gguf-inference \\"
echo "     python3 inference.py $MODEL_PATH --interactive"
echo ""

echo "2. Single Prompt"
echo "   docker run --rm \\"
echo "     -v \$(pwd)/models:/app/models:ro \\"
echo "     gguf-inference \\"
echo "     python3 inference.py $MODEL_PATH \\"
echo "     --prompt 'Hello, how are you today?'"
echo ""

echo "3. With Configuration File"
echo "   docker run --rm \\"
echo "     -v \$(pwd)/models:/app/models:ro \\"
echo "     -v \$(pwd)/configs:/app/configs:ro \\"
echo "     gguf-inference \\"
echo "     python3 inference.py $MODEL_PATH \\"
echo "     --config /app/configs/example_config.json \\"
echo "     --prompt 'Explain quantum computing'"
echo ""

echo "4. Streaming Output"
echo "   docker run --rm \\"
echo "     -v \$(pwd)/models:/app/models:ro \\"
echo "     gguf-inference \\"
echo "     python3 inference.py $MODEL_PATH \\"
echo "     --prompt 'Write a short story about AI' \\"
echo "     --stream --max-tokens 200"
echo ""

echo "5. Docker Compose (Recommended)"
echo "   # Edit docker-compose.yml to set your model path"
echo "   docker-compose up -d"
echo "   docker-compose exec gguf-inference bash"
echo ""

echo "6. GPU Support (if available)"
echo "   docker run --gpus all -it --rm \\"
echo "     -v \$(pwd)/models:/app/models:ro \\"
echo "     gguf-inference \\"
echo "     python3 inference.py $MODEL_PATH \\"
echo "     --interactive --n-gpu-layers 35"
echo ""

# Interactive menu
while true; do
    echo ""
    print_header "Quick Actions"
    echo "a) Run interactive mode"
    echo "b) Test with sample prompt"
    echo "c) Show help"
    echo "d) Build/rebuild image"
    echo "e) Clean up Docker"
    echo "q) Quit"
    echo ""
    read -p "Choose an option (a-e, q): " choice

    case $choice in
        a)
            if [ -z "$(find ./models -name "*.gguf" 2>/dev/null)" ]; then
                print_error "No GGUF model files found. Please add models to ./models/ directory first."
                continue
            fi
            print_status "Starting interactive mode..."
            docker run -it --rm \
                -v $(pwd)/models:/app/models:ro \
                -v $(pwd)/outputs:/app/outputs \
                gguf-inference \
                python3 inference.py $MODEL_PATH --interactive
            ;;
        b)
            if [ -z "$(find ./models -name "*.gguf" 2>/dev/null)" ]; then
                print_error "No GGUF model files found. Please add models to ./models/ directory first."
                continue
            fi
            print_status "Running sample prompt..."
            docker run --rm \
                -v $(pwd)/models:/app/models:ro \
                gguf-inference \
                python3 inference.py $MODEL_PATH \
                --prompt "Hello! Can you tell me a fun fact?" \
                --max-tokens 100
            ;;
        c)
            print_status "Showing help..."
            docker run --rm gguf-inference python3 inference.py --help
            ;;
        d)
            print_status "Building/rebuilding Docker image..."
            docker build --no-cache -t gguf-inference .
            print_status "Image rebuilt successfully!"
            ;;
        e)
            print_warning "This will remove all unused Docker resources..."
            read -p "Are you sure? (y/N): " confirm
            if [[ $confirm == [yY] ]]; then
                docker system prune -f
                print_status "Docker cleanup completed!"
            fi
            ;;
        q)
            print_status "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid option. Please choose a-e or q."
            ;;
    esac
done