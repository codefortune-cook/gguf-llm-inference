#!/usr/bin/env python3
import torch
import subprocess
import sys

def check_gpu_info():
    print("=== GPU Information Check ===\n")
    
    # Check if CUDA is available
    print(f"CUDA Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"PyTorch Version: {torch.__version__}")
        
        # Get GPU count and info
        gpu_count = torch.cuda.device_count()
        print(f"Number of GPUs: {gpu_count}")
        
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_capability = torch.cuda.get_device_capability(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3  # Convert to GB
            
            print(f"\nGPU {i}: {gpu_name}")
            print(f"  CUDA Capability: {gpu_capability[0]}.{gpu_capability[1]}")
            print(f"  Memory: {gpu_memory:.1f} GB")
            
            # Check if this GPU is compatible with current PyTorch
            if gpu_capability[0] >= 5:  # sm_50 and above
                print(f"  Status: ✅ Compatible with current PyTorch")
            else:
                print(f"  Status: ❌ Not compatible with current PyTorch")
    else:
        print("No CUDA-capable GPU found or CUDA not properly installed.")
    
    print("\n=== System Information ===")
    
    # Try to get more detailed GPU info using nvidia-smi
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version,compute_cap', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("NVIDIA-SMI Output:")
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"  {line}")
        else:
            print("nvidia-smi not available or failed")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("nvidia-smi not found or timed out")
    
    print("\n=== PyTorch CUDA Support ===")
    print(f"PyTorch built with CUDA: {torch.version.cuda is not None}")
    if torch.version.cuda:
        print(f"PyTorch CUDA version: {torch.version.cuda}")
    
    # Check for common CUDA capability support
    print("\n=== CUDA Capability Support ===")
    supported_capabilities = [
        (5, 0, "sm_50"),
        (6, 0, "sm_60"), 
        (7, 0, "sm_70"),
        (7, 5, "sm_75"),
        (8, 0, "sm_80"),
        (8, 6, "sm_86"),
        (9, 0, "sm_90")
    ]
    
    print("PyTorch supports the following CUDA capabilities:")
    for major, minor, name in supported_capabilities:
        print(f"  {name} ({major}.{minor})")
    
    if torch.cuda.is_available():
        current_cap = torch.cuda.get_device_capability(0)
        print(f"\nYour GPU capability: {current_cap[0]}.{current_cap[1]} (sm_{current_cap[0]}{current_cap[1]})")
        
        if current_cap[0] > 9 or (current_cap[0] == 9 and current_cap[1] > 0):
            print("⚠️  Your GPU has newer CUDA capability than PyTorch supports!")
            print("   This may cause compatibility issues with certain operations.")
        elif current_cap[0] >= 5:
            print("✅ Your GPU is compatible with current PyTorch")
        else:
            print("❌ Your GPU is not compatible with current PyTorch")

if __name__ == "__main__":
    check_gpu_info()
