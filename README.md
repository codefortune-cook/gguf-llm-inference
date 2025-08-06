# GGUF & llama.cpp 

This project helps you to inference GGUF models with llama.cpp. 

## Local Docker Images

The following table lists the local Docker images available in the `docker-images` directory:

| Image Name         | Dockerfile Path                  | Description                        |
|--------------------|----------------------------------|------------------------------------|
| llama-cpp:full   | docker-images/llama-cpp_full.tar      | Docker image to inference GGUF model using CPU & RAM |
| llama-cpp:full-cuda | docker-images/llama-cpp_full_cuda.tar | Docker image to inference GGUF model using GPU |
| llama-cpp:server-cuda | docker-images/llama-cpp_server_cuda.tar | Docker image to inference GGUF model using GPU on webui |

## Load Images into System
docker load < <docker-image-file-path>

## Usage
**Inference with GPU**
```shell
sudo docker run --gpus all -v  ./models:/app/models ghcr.io/ggml-org/llama.cpp:full-cuda \
--run -m /app/models/unsloth/gpt-oss-20b-GGUF/gpt-oss-20b-F32.gguf \
-p "Building a website can be done in 10 simple steps:" -n 512
```

**Command to run llama.cpp as server**
```bash
sudo docker run --gpus all -v ./models:/app/models -p 8000:8000 ghcr.io/ggml-org/llama.cpp:server-cuda \
 -m /app/models/unsloth/gpt-oss-20b-GGUF/gpt-oss-20b-F32.gguf \
 --port 8000 --host 0.0.0.0 -n 512
```