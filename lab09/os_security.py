"""Set a file to read-only and observe the OS permission check (Lab 9)."""
import os
import stat


def main():
    secure_file = "secret_config.json"
    if os.path.exists(secure_file):
        os.chmod(secure_file, 0o666)
        os.remove(secure_file)

    with open(secure_file, "w", encoding="utf-8") as f:
        f.write("{'api_key': 'replace-with-a-test-value'}")

    print(f"Created {secure_file}.")
    print("Locking file permissions to Read-Only (0o400)...")
    os.chmod(secure_file, 0o400)
    print(f"New Permissions: {stat.filemode(os.stat(secure_file).st_mode)}")
    print("\nAttempting to overwrite the file...")
    try:
        with open(secure_file, "a", encoding="utf-8") as f:
            f.write("\nTEST WRITE")
        print("Write succeeded for this process.")
        print("Note: elevated/root users may bypass ordinary permission checks.")
    except PermissionError as exc:
        print(f">>> [OS KERNEL BLOCKED] PermissionError: {exc}")
        print(">>> The operating system denied the write.")


if __name__ == "__main__":
    main()
