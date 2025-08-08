FROM daturaai/pytorch:2.6.0-py3.12-cuda12.6.3-devel-ubuntu24.04

RUN pip install --break-system-packages transformers sentencepiece safetensors bitsandbytes huggingface-hub

