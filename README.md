# Docker Usage Guide for GGUF LLM Inference

This guide explains how to use the Dockerized GGUF LLM inference system on Windows WSL.

## Prerequisites

1. **Docker Desktop for Windows** with WSL2 integration enabled
2. **GGUF model files** (e.g., from Hugging Face)

## Quick Start

### 1. Download a GGUF Model

Place your GGUF model files in the `models/` directory:

```bash
# Example: Download a model from Hugging Face
mkdir -p models
cd models
wget https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/pytorch_model.bin.gguf
# Or use your own GGUF model files
cd ..
```

### 2. Build the Docker Image

```bash
docker build -t gguf-inference .
```

### 3. Run with Docker Compose (Recommended)

```bash
# Edit docker-compose.yml to specify your model path
# Then run:
docker-compose up -d

# For interactive mode:
docker-compose exec gguf-inference bash
```

### 4. Run Directly with Docker

```bash
# Interactive mode
docker run -it --rm \
  -v $(pwd)/models:/app/models:ro \
  -v $(pwd)/configs:/app/configs:ro \
  -v $(pwd)/outputs:/app/outputs \
  gguf-inference \
  python3 inference.py /app/models/your-model.gguf --interactive

# Single prompt
docker run --rm \
  -v $(pwd)/models:/app/models:ro \
  gguf-inference \
  python3 inference.py /app/models/your-model.gguf \
  --prompt "Hello, how are you today?"
```

## Usage Examples

### Basic Text Generation

```bash
docker run --rm \
  -v $(pwd)/models:/app/models:ro \
  gguf-inference \
  python3 inference.py /app/models/your-model.gguf \
  --prompt "The future of AI is" \
  --max-tokens 100 \
  --temperature 0.8
```

### Interactive Chat

```bash
docker run -it --rm \
  -v $(pwd)/models:/app/models:ro \
  gguf-inference \
  python3 inference.py /app/models/your-model.gguf \
  --interactive \
  --n-ctx 4096
```

### Using Configuration File

```bash
docker run --rm \
  -v $(pwd)/models:/app/models:ro \
  -v $(pwd)/configs:/app/configs:ro \
  gguf-inference \
  python3 inference.py /app/models/your-model.gguf \
  --config /app/configs/example_config.json \
  --prompt "Tell me about quantum computing"
```

### GPU Support (if available)

For GPU support, you need NVIDIA Container Toolkit:

```bash
# Install nvidia-container-toolkit first
# Then run with GPU support:
docker run --gpus all -it --rm \
  -v $(pwd)/models:/app/models:ro \
  gguf-inference \
  python3 inference.py /app/models/your-model.gguf \
  --interactive \
  --n-gpu-layers 35
```

## Configuration Options

### Command Line Arguments

- `--prompt, -p`: Input prompt for generation
- `--interactive, -i`: Run in interactive chat mode
- `--config, -c`: Path to JSON configuration file
- `--max-tokens`: Maximum tokens to generate (default: 256)
- `--temperature`: Sampling temperature (default: 0.7)
- `--top-p`: Top-p sampling (default: 0.9)
- `--top-k`: Top-k sampling (default: 40)
- `--repeat-penalty`: Repetition penalty (default: 1.1)
- `--n-ctx`: Context length (default: 2048)
- `--n-gpu-layers`: Number of GPU layers (default: 0)
- `--n-threads`: Number of CPU threads (default: auto)
- `--stream`: Enable streaming output
- `--verbose, -v`: Enable verbose output

### Configuration File Format

See `configs/example_config.json` for a complete example:

```json
{
  "model": {
    "n_ctx": 4096,
    "n_threads": -1,
    "n_gpu_layers": 0,
    "verbose": false
  },
  "generation": {
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "repeat_penalty": 1.1,
    "stream": false
  }
}
```

## Directory Structure

```
gguf-llm-inference/
├── inference.py          # Main inference script
├── Dockerfile           # Docker build instructions
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
├── models/             # Your GGUF model files (mounted volume)
├── configs/            # Configuration files (mounted volume)
│   └── example_config.json
└── outputs/            # Output files (mounted volume)
```

## Troubleshooting

### Common Issues

1. **Model not found**: Ensure your model file is in the `models/` directory and the path is correct.

2. **Permission denied**: The container runs as a non-root user. Ensure your model files are readable:
   ```bash
   chmod 644 models/*.gguf
   ```

3. **Out of memory**: Reduce context length or use a smaller model:
   ```bash
   --n-ctx 1024
   ```

4. **Slow performance**: Try adjusting CPU threads:
   ```bash
   --n-threads 8  # or your CPU core count
   ```

### Docker Commands

```bash
# View logs
docker-compose logs gguf-inference

# Stop services
docker-compose down

# Rebuild image
docker-compose build --no-cache

# Access container shell
docker-compose exec gguf-inference bash

# Remove all containers and images
docker system prune -a
```

## Performance Tips

1. **CPU Optimization**: Set `--n-threads` to your CPU core count
2. **Memory**: Use appropriate `--n-ctx` for your available RAM
3. **GPU**: If available, use `--n-gpu-layers` for faster inference
4. **Model Size**: Smaller quantized models (Q4, Q5) are faster but less accurate

## Security Notes

- The container runs as a non-root user for security
- Model files are mounted read-only
- Only necessary ports are exposed
- Use trusted model sources only