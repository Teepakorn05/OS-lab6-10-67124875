"""Compare many small-file reads with sequential packed-file reads (Lab 8)."""
import os
import time


def setup_test_files(num_files, file_size_bytes):
    print("Setting up test environments...")
    os.makedirs("raw_images_folder", exist_ok=True)
    for i in range(num_files):
        with open(f"raw_images_folder/img_{i}.bin", "wb") as f:
            f.write(b"\x00" * file_size_bytes)
    with open("packed_dataset.tfrecord", "wb") as f:
        f.write(b"\x00" * (num_files * file_size_bytes))
    print("Setup complete.\n")


def test_random_small_files(num_files):
    print(f"Test 1: Reading {num_files} separate small files")
    start_time = time.perf_counter()
    for i in range(num_files):
        with open(f"raw_images_folder/img_{i}.bin", "rb") as f:
            f.read()
    elapsed = time.perf_counter() - start_time
    print(f"-> Time Taken: {elapsed:.4f} seconds")
    return elapsed


def test_sequential_large_file(num_files, file_size_bytes):
    print("\nTest 2: Reading one packed file sequentially")
    start_time = time.perf_counter()
    with open("packed_dataset.tfrecord", "rb") as f:
        for _ in range(num_files):
            f.read(file_size_bytes)
    elapsed = time.perf_counter() - start_time
    print(f"-> Time Taken: {elapsed:.4f} seconds")
    return elapsed


def cleanup(num_files):
    for i in range(num_files):
        path = f"raw_images_folder/img_{i}.bin"
        if os.path.exists(path):
            os.remove(path)
    if os.path.isdir("raw_images_folder"):
        os.rmdir("raw_images_folder")
    if os.path.exists("packed_dataset.tfrecord"):
        os.remove("packed_dataset.tfrecord")


def main():
    num_files = 1000
    file_size = 4096
    setup_test_files(num_files, file_size)
    try:
        test_random_small_files(num_files)
        test_sequential_large_file(num_files, file_size)
    finally:
        cleanup(num_files)


if __name__ == "__main__":
    main()
