import torch
import multiprocessing
import signal
import sys

# --- CPU Stress Function ---
def stress_cpu():
    # Using matrix multiplication instead of 'pass' for actual thermal load
    print("CPU Stress worker started.")
    while True:
        # Generate random tensors and multiply them
        a = torch.randn(2000, 2000)
        b = torch.randn(2000, 2000)
        _ = torch.mm(a, b)

# --- GPU Stress Function ---
def stress_gpu():
    if not torch.cuda.is_available():
        print("CUDA not found. Skipping GPU stress.")
        return

    device = torch.device("cuda")
    print(f"GPU Stress started on: {torch.cuda.get_device_name(0)}")
    
    # Move large tensors to the GPU
    # Size adjusted to fill VRAM and keep the cores busy
    a = torch.randn(5000, 5000, device=device)
    b = torch.randn(5000, 5000, device=device)
    
    while True:
        # Continuous matrix multiplication on GPU
        _ = torch.mm(a, b)

if __name__ == '__main__':
    num_cores = multiprocessing.cpu_count()
    processes = []

    print(f"--- Starting Stress Test ---")
    print(f"Targeting {num_cores} CPU cores and 1 GPU.")
    print("Press Ctrl+C to stop.")

    try:
        # Start CPU processes
        for _ in range(num_cores):
            p = multiprocessing.Process(target=stress_cpu)
            p.start()
            processes.append(p)

        # Start GPU process
        g = multiprocessing.Process(target=stress_gpu)
        g.start()
        processes.append(g)

        # Keep the main thread alive
        for p in processes:
            p.join()

    except KeyboardInterrupt:
        print("\nStopping stress test... cleaning up processes.")
        for p in processes:
            p.terminate()
        sys.exit(0)
