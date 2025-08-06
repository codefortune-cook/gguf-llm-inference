# #!/usr/bin/env python3
# """
# GGUF LLM Inference Script
# A comprehensive script for running inference on GGUF format language models.
# """

# import argparse
# import json
# import os
# import sys
# from pathlib import Path
# from typing import Dict, List, Optional, Union

# try:
#     from llama_cpp import Llama
# except ImportError:
#     print("Error: llama-cpp-python is not installed. Install it with: pip install llama-cpp-python")
#     sys.exit(1)


# class GGUFInference:
#     """GGUF model inference handler."""
    
#     def __init__(
#         self,
#         model_path: str,
#         n_ctx: int = 2048,
#         n_threads: int = -1,
#         n_gpu_layers: int = 0,
#         verbose: bool = False,
#         **kwargs
#     ):
#         """
#         Initialize the GGUF inference engine.
        
#         Args:
#             model_path: Path to the GGUF model file
#             n_ctx: Context length (default: 2048)
#             n_threads: Number of CPU threads (-1 for auto)
#             n_gpu_layers: Number of layers to offload to GPU
#             verbose: Enable verbose output
#             **kwargs: Additional arguments for Llama model
#         """
#         self.model_path = Path(model_path)
#         if not self.model_path.exists():
#             raise FileNotFoundError(f"Model file not found: {model_path}")
        
#         print(f"Loading model: {self.model_path}")
#         print(f"Context length: {n_ctx}")
#         print(f"GPU layers: {n_gpu_layers}")
        
#         try:
#             self.llm = Llama(
#                 model_path=str(self.model_path),
#                 n_ctx=n_ctx,
#                 n_threads=n_threads,
#                 n_gpu_layers=n_gpu_layers,
#                 verbose=verbose,
#                 **kwargs
#             )
#             print("Model loaded successfully!")
#         except Exception as e:
#             print(f"Error loading model: {e}")
#             self.llm = None
#             raise
    
#     def generate(
#         self,
#         prompt: str,
#         max_tokens: int = 256,
#         temperature: float = 0.7,
#         top_p: float = 0.9,
#         top_k: int = 40,
#         repeat_penalty: float = 1.1,
#         stop: Optional[List[str]] = None,
#         stream: bool = False,
#         **kwargs
#     ) -> Union[str, Dict]:
#         """
#         Generate text from the model.
        
#         Args:
#             prompt: Input prompt
#             max_tokens: Maximum tokens to generate
#             temperature: Sampling temperature
#             top_p: Top-p sampling
#             top_k: Top-k sampling
#             repeat_penalty: Repetition penalty
#             stop: Stop sequences
#             stream: Enable streaming output
#             **kwargs: Additional generation parameters
            
#         Returns:
#             Generated text or response dictionary
#         """
#         try:
#             if stream:
#                 return self._generate_stream(
#                     prompt, max_tokens, temperature, top_p, top_k, 
#                     repeat_penalty, stop, **kwargs
#                 )
#             else:
#                 response = self.llm(
#                     prompt,
#                     max_tokens=max_tokens,
#                     temperature=temperature,
#                     top_p=top_p,
#                     top_k=top_k,
#                     repeat_penalty=repeat_penalty,
#                     stop=stop or [],
#                     **kwargs
#                 )
#                 return response['choices'][0]['text']
#         except Exception as e:
#             print(f"Error during generation: {e}")
#             raise
    
#     def _generate_stream(self, prompt: str, max_tokens: int, temperature: float,
#                         top_p: float, top_k: int, repeat_penalty: float,
#                         stop: Optional[List[str]], **kwargs):
#         """Generate text with streaming output."""
#         stream = self.llm(
#             prompt,
#             max_tokens=max_tokens,
#             temperature=temperature,
#             top_p=top_p,
#             top_k=top_k,
#             repeat_penalty=repeat_penalty,
#             stop=stop or [],
#             stream=True,
#             **kwargs
#         )
        
#         full_response = ""
#         for output in stream:
#             token = output['choices'][0]['text']
#             full_response += token
#             print(token, end='', flush=True)
        
#         print()  # New line after streaming
#         return full_response
    
#     def chat(
#         self,
#         messages: List[Dict[str, str]],
#         max_tokens: int = 256,
#         temperature: float = 0.7,
#         **kwargs
#     ) -> str:
#         """
#         Chat interface for conversational models.
        
#         Args:
#             messages: List of message dictionaries with 'role' and 'content'
#             max_tokens: Maximum tokens to generate
#             temperature: Sampling temperature
#             **kwargs: Additional generation parameters
            
#         Returns:
#             Assistant's response
#         """
#         # Convert messages to prompt format
#         prompt = self._format_chat_prompt(messages)
#         return self.generate(
#             prompt, max_tokens=max_tokens, temperature=temperature, **kwargs
#         )
    
#     def _format_chat_prompt(self, messages: List[Dict[str, str]]) -> str:
#         """Format chat messages into a prompt."""
#         formatted_prompt = ""
#         for message in messages:
#             role = message.get('role', 'user')
#             content = message.get('content', '')
            
#             if role == 'system':
#                 formatted_prompt += f"System: {content}\n\n"
#             elif role == 'user':
#                 formatted_prompt += f"User: {content}\n\n"
#             elif role == 'assistant':
#                 formatted_prompt += f"Assistant: {content}\n\n"
        
#         formatted_prompt += "Assistant: "
#         return formatted_prompt


# def load_config(config_path: str) -> Dict:
#     """Load configuration from JSON file."""
#     try:
#         with open(config_path, 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         print(f"Config file not found: {config_path}")
#         return {}
#     except json.JSONDecodeError as e:
#         print(f"Error parsing config file: {e}")
#         return {}


# def interactive_mode(inference_engine: GGUFInference):
#     """Run interactive chat mode."""
#     print("\n" + "="*50)
#     print("Interactive Chat Mode")
#     print("Type 'quit' or 'exit' to end the session")
#     print("Type 'clear' to clear chat history")
#     print("="*50 + "\n")
    
#     chat_history = []
    
#     while True:
#         try:
#             user_input = input("\nYou: ").strip()
            
#             if user_input.lower() in ['quit', 'exit']:
#                 print("Goodbye!")
#                 break
#             elif user_input.lower() == 'clear':
#                 chat_history = []
#                 print("Chat history cleared.")
#                 continue
#             elif not user_input:
#                 continue
            
#             chat_history.append({"role": "user", "content": user_input})
            
#             print("\nAssistant: ", end='')
#             response = inference_engine.generate(
#                 inference_engine._format_chat_prompt(chat_history),
#                 stream=True,
#                 stop=["\nUser:", "\nYou:"]
#             )
            
#             chat_history.append({"role": "assistant", "content": response.strip()})
            
#         except KeyboardInterrupt:
#             print("\nGoodbye!")
#             break
#         except Exception as e:
#             print(f"\nError: {e}")


# def main():
#     """Main function."""
#     parser = argparse.ArgumentParser(description="GGUF LLM Inference Script")
#     parser.add_argument("model_path", help="Path to the GGUF model file")
#     parser.add_argument("--prompt", "-p", help="Prompt for generation")
#     parser.add_argument("--config", "-c", help="Configuration file path")
#     parser.add_argument("--interactive", "-i", action="store_true", 
#                        help="Run in interactive mode")
#     parser.add_argument("--max-tokens", type=int, default=256,
#                        help="Maximum tokens to generate (default: 256)")
#     parser.add_argument("--temperature", type=float, default=0.7,
#                        help="Sampling temperature (default: 0.7)")
#     parser.add_argument("--top-p", type=float, default=0.9,
#                        help="Top-p sampling (default: 0.9)")
#     parser.add_argument("--top-k", type=int, default=40,
#                        help="Top-k sampling (default: 40)")
#     parser.add_argument("--repeat-penalty", type=float, default=1.1,
#                        help="Repetition penalty (default: 1.1)")
#     parser.add_argument("--n-ctx", type=int, default=2048,
#                        help="Context length (default: 2048)")
#     parser.add_argument("--n-gpu-layers", type=int, default=0,
#                        help="Number of GPU layers (default: 0)")
#     parser.add_argument("--n-threads", type=int, default=-1,
#                        help="Number of CPU threads (default: auto)")
#     parser.add_argument("--stream", action="store_true",
#                        help="Enable streaming output")
#     parser.add_argument("--verbose", "-v", action="store_true",
#                        help="Enable verbose output")
    
#     args = parser.parse_args()
    
#     # Load configuration if provided
#     config = {}
#     if args.config:
#         config = load_config(args.config)
    
#     # Merge command line args with config
#     model_args = {
#         'n_ctx': args.n_ctx,
#         'n_threads': args.n_threads,
#         'n_gpu_layers': args.n_gpu_layers,
#         'verbose': args.verbose,
#         **config.get('model', {})
#     }
    
#     generation_args = {
#         'max_tokens': args.max_tokens,
#         'temperature': args.temperature,
#         'top_p': args.top_p,
#         'top_k': args.top_k,
#         'repeat_penalty': args.repeat_penalty,
#         'stream': args.stream,
#         **config.get('generation', {})
#     }
    
#     try:
#         # Initialize inference engine
#         inference_engine = GGUFInference(args.model_path, **model_args)
        
#         if args.interactive:
#             interactive_mode(inference_engine)
#         elif args.prompt:
#             print("Generating response...\n")
#             response = inference_engine.generate(args.prompt, **generation_args)
#             if not args.stream:
#                 print(response)
#         else:
#             print("No prompt provided. Use --prompt or --interactive mode.")
            
#     except Exception as e:
#         print(f"Error: {e}")
#         sys.exit(1)


# if __name__ == "__main__":
#     main()



from llama_cpp import Llama

model_path = "/app/models/unsloth/gpt-oss-20b-GGUF/gpt-oss-20b-F32.gguf"
llm = Llama(
    model_path=model_path,
    n_ctx=16384,
    n_gpu_layers=0,       # set -1 if you built with GPU support
    verbose=True,
)

# 3) Chat
resp = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Give me 3 bullet points about GPT-OSS-20B."}
    ],
    temperature=0.5,
    max_tokens=256,
)

print(resp["choices"][0]["message"]["content"])