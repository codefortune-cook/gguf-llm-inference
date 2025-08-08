import argparse, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

def load_model(model_id: str, load_in_4bit: bool = False, force_cpu: bool = False):
    dtype = torch.bfloat16 if torch.cuda.is_available() and not force_cpu else torch.float32
    quant = None
    if load_in_4bit:
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=dtype)

    tok = AutoTokenizer.from_pretrained(model_id, use_fast=True)
    
    # Handle device mapping based on force_cpu flag
    if force_cpu:
        device_map = "cpu"
    else:
        device_map = "auto"
    
    # Only pass quantization_config if it's not None
    kwargs = {
        "device_map": device_map,
        "torch_dtype": dtype,
        "low_cpu_mem_usage": True,
    }
    if quant is not None:
        kwargs["quantization_config"] = quant
    
    try:
        mdl = AutoModelForCausalLM.from_pretrained(model_id, **kwargs)
    except RuntimeError as e:
        if "CUDA error" in str(e) or "no kernel image" in str(e):
            print("CUDA compatibility issue detected. Trying with CPU offloading...")
            # Force CPU offloading as fallback
            kwargs["device_map"] = "cpu"
            kwargs["torch_dtype"] = torch.float32
            mdl = AutoModelForCausalLM.from_pretrained(model_id, **kwargs)
        else:
            raise e
    
    return tok, mdl

def to_chat_prompt(tok, user_msg: str):
    # If the model has a chat template, use it; else fall back to raw text
    msgs = [{"role": "user", "content": user_msg}]
    if hasattr(tok, "apply_chat_template"):
        return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    return user_msg

def generate(tok, mdl, prompt: str, max_new_tokens=256, temperature=0.7, top_p=0.9):
    inputs = tok(prompt, return_tensors="pt")
    inputs = {k: v.to(mdl.device) for k, v in inputs.items()}
    with torch.no_grad():
        out = mdl.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            pad_token_id=tok.eos_token_id,
        )
    text = tok.decode(out[0], skip_special_tokens=True)
    return text

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="HF model id")
    ap.add_argument("--prompt", required=True, help="User prompt")
    ap.add_argument("--q4", action="store_true", help="Load in 4-bit (bitsandbytes)")
    ap.add_argument("--cpu", action="store_true", help="Force CPU usage (for CUDA compatibility issues)")
    ap.add_argument("--max_new_tokens", type=int, default=256)
    args = ap.parse_args()

    tok, mdl = load_model(args.model, load_in_4bit=args.q4, force_cpu=args.cpu)
    prompt = to_chat_prompt(tok, args.prompt)
    text = generate(tok, mdl, prompt, max_new_tokens=args.max_new_tokens)
    # Print only the model's reply if a chat template duplicated the prompt
    print(text)

if __name__ == "__main__":
    main()
