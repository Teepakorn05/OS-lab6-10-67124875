"""Contrast in-memory updates with repeated disk I/O (Lab 6 illustration)."""
import os
import time


def fast_ram_access(iterations):
    simulated_ram = [0.0] * 1000
    start_time = time.time()
    for _ in range(iterations):
        for i in range(len(simulated_ram)):
            simulated_ram[i] += 1.5
    return time.time() - start_time


def slow_swap_thrashing_access(iterations, filename="swap_file.bin"):
    with open(filename, "wb") as f:
        f.write(b"\x00" * 1000)

    start_time = time.time()
    try:
        for _ in range(iterations):
            with open(filename, "r+b") as f:
                data = bytearray(f.read())
                for i in range(len(data)):
                    data[i] = (data[i] + 1) % 255
                f.seek(0)
                f.write(data)
    finally:
        if os.path.exists(filename):
            os.remove(filename)
    return time.time() - start_time


def main():
    iterations = 10000
    print(f"--- Simulating AI Training Batch ({iterations:,} Iterations) ---")
    ram_time = fast_ram_access(iterations)
    print(f"\n1. Scenario: Batch fits in RAM\n   -> Processing Time: {ram_time:.4f} seconds")
    swap_time = slow_swap_thrashing_access(iterations)
    print(f"\n2. Scenario: Repeated disk access\n   -> Processing Time: {swap_time:.4f} seconds")
    if ram_time > 0:
        print(f"\n>>> This file-I/O simulation took {swap_time / ram_time:.0f} times as long.")
    print("Note: This illustrates I/O overhead; it is not a benchmark of the OS swap subsystem.")


if __name__ == "__main__":
    main()
