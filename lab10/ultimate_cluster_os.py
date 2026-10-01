"""A teaching simulator for queued AI jobs, RAM and GPU allocation (Lab 10)."""
import os
import queue
import threading
import time


class AIClusterOS:
    def __init__(self, total_ram_gb, num_gpus):
        self.total_ram_gb = total_ram_gb
        self.available_ram_gb = total_ram_gb
        self.ram_lock = threading.Lock()
        self.status_lock = threading.Lock()
        self.gpu_locks = {i: threading.Lock() for i in range(num_gpus)}
        self.gpu_status = {i: "IDLE" for i in range(num_gpus)}
        self.job_queue = queue.Queue()
        self.active_jobs = set()
        self.is_running = True
        self.dashboard_thread = threading.Thread(target=self._dashboard_loop, daemon=True)
        self.scheduler_thread = threading.Thread(target=self._os_scheduler_loop)
        self.dashboard_thread.start()
        self.scheduler_thread.start()

    def _dashboard_loop(self):
        while self.is_running:
            time.sleep(1.5)
            with self.ram_lock, self.status_lock:
                ram_text = f"{self.available_ram_gb}/{self.total_ram_gb} GB"
                gpu_text = " | ".join(f"GPU {i}: {self.gpu_status[i]}" for i in self.gpu_locks)
                active_text = ", ".join(sorted(self.active_jobs)) or "none"
            print("\n" + "=" * 54)
            print(f"[LIVE DASHBOARD] RAM Available: {ram_text}")
            print(f"[LIVE DASHBOARD] {gpu_text}")
            print(f"[LIVE DASHBOARD] Queue: {self.job_queue.qsize()} | Active: {active_text}")
            print("=" * 54 + "\n")

    def submit_job(self, job_name, dataset_path, req_ram, req_gpus, duration):
        self.job_queue.put((job_name, dataset_path, req_ram, req_gpus, duration))
        print(f"[API] Submitted: {job_name} -> queued.")

    def _os_scheduler_loop(self):
        while self.is_running or not self.job_queue.empty():
            try:
                job_data = self.job_queue.get(timeout=0.5)
            except queue.Empty:
                continue
            worker = threading.Thread(target=self._execute_job, args=job_data)
            worker.start()

    def _execute_job(self, job_name, dataset_path, req_ram, req_gpus, duration):
        acquired_gpus = []
        allocated_ram = False
        try:
            # This is an existence check, not a full permission/ACL check.
            if not os.path.exists(dataset_path):
                print(f"[REJECTED] {job_name}: dataset '{dataset_path}' not found.")
                return
            if req_ram > self.total_ram_gb:
                print(f"[REJECTED] {job_name}: RAM request exceeds total RAM.")
                return
            if any(gpu not in self.gpu_locks for gpu in req_gpus):
                print(f"[REJECTED] {job_name}: unknown GPU requested.")
                return

            with self.status_lock:
                self.active_jobs.add(job_name)
            print(f"[{job_name}] Waiting for {req_ram} GB RAM...")
            while True:
                with self.ram_lock:
                    if self.available_ram_gb >= req_ram:
                        self.available_ram_gb -= req_ram
                        allocated_ram = True
                        break
                time.sleep(0.2)
            print(f"[{job_name}] Allocated {req_ram} GB RAM.")

            # Consistent lock ordering prevents circular wait among GPU locks.
            sorted_gpus = sorted(set(req_gpus))
            for gpu in sorted_gpus:
                self.gpu_locks[gpu].acquire()
                acquired_gpus.append(gpu)
                with self.status_lock:
                    self.gpu_status[gpu] = f"BUSY ({job_name})"

            print(f"[{job_name}] Running with GPUs {sorted_gpus or 'none'}.")
            time.sleep(duration)
            print(f"[{job_name}] Finished successfully.")
        finally:
            for gpu in reversed(acquired_gpus):
                with self.status_lock:
                    self.gpu_status[gpu] = "IDLE"
                self.gpu_locks[gpu].release()
            if allocated_ram:
                with self.ram_lock:
                    self.available_ram_gb += req_ram
            with self.status_lock:
                self.active_jobs.discard(job_name)
            self.job_queue.task_done()

    def shutdown(self):
        self.job_queue.join()
        self.is_running = False
        self.scheduler_thread.join()
        self.dashboard_thread.join(timeout=2.0)
        print("\n=== Cluster OS Shutdown Gracefully ===")


def main():
    dataset_path = "secure_dataset.csv"
    with open(dataset_path, "w", encoding="utf-8") as f:
        f.write("demo data\n")

    print("=== Booting AI Cluster OS (64 GB RAM, 4 GPUs) ===")
    cluster = AIClusterOS(total_ram_gb=64, num_gpus=4)
    cluster.submit_job("Workload_A_Training", dataset_path, req_ram=40, req_gpus=[2, 1, 0], duration=8)
    time.sleep(1)
    cluster.submit_job("Workload_B_Preprocessing", dataset_path, req_ram=16, req_gpus=[], duration=6)
    time.sleep(1)
    cluster.submit_job("Workload_C_Inference", dataset_path, req_ram=2, req_gpus=[3], duration=3)
    time.sleep(1)
    cluster.submit_job("Workload_D_MissingDataset", "secret_keys.txt", req_ram=1, req_gpus=[], duration=1)
    cluster.shutdown()
    os.remove(dataset_path)


if __name__ == "__main__":
    main()
