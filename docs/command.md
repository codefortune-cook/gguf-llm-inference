```shell
sudo docker run -v ./models:/app/models ghcr.io/ggml-org/llama.cpp:full-cuda \
--run -m /app/models/unsloth/gpt-oss-20b-GGUF/gpt-oss-20b-F32.gguf \
-p "Building a website can be done in 10 simple steps:" -n 512
```

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