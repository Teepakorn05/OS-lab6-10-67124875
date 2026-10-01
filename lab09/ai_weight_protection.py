"""Demonstrate read-only permissions for a model-weight file (Lab 9)."""
import os


def simulate_hpc_cluster():
    weight_file = "production_resnet50.pth"
    if os.path.exists(weight_file):
        os.chmod(weight_file, 0o666)
        os.remove(weight_file)

    print("Creating a small dummy model-weight file for this simulation...")
    with open(weight_file, "wb") as f:
        f.write(b"demo-weight-data")

    print("Setting model weights to read-only for all users (0o444)...")
    os.chmod(weight_file, 0o444)
    print("Attempting a write as the current process...")
    try:
        with open(weight_file, "wb") as model:
            model.write(b"attempted-overwrite")
        print("Write succeeded for this process.")
        print("If running as root/administrator, permissions may be bypassed.")
    except PermissionError:
        print(">>> [DISASTER AVERTED] OS denied write access.")


if __name__ == "__main__":
    simulate_hpc_cluster()
