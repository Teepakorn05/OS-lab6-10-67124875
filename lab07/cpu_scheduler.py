"""Compare FCFS and Round Robin waiting/turnaround times (Lab 7)."""
from collections import deque


def simulate_fcfs(processes):
    print("\n--- Running FCFS Scheduler ---")
    current_time = 0
    total_wait_time = 0
    total_turnaround_time = 0

    for pid, burst_time in processes:
        wait_time = current_time
        total_wait_time += wait_time
        turnaround_time = wait_time + burst_time
        total_turnaround_time += turnaround_time
        print(f"[Time {current_time:02d}] Process {pid} starts. (Wait time: {wait_time})")
        current_time += burst_time
        print(f"[Time {current_time:02d}] Process {pid} finishes. (Turnaround time: {turnaround_time})")

    count = len(processes)
    print(f">> FCFS Average Waiting Time: {total_wait_time / count:.2f}")
    print(f">> FCFS Average Turnaround Time: {total_turnaround_time / count:.2f}")


def simulate_round_robin(processes, quantum):
    if quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")

    print(f"\n--- Running Round Robin Scheduler (Quantum = {quantum}) ---")
    remaining = {pid: burst for pid, burst in processes}
    wait_times = {pid: 0 for pid, _ in processes}
    last_run_time = {pid: 0 for pid, _ in processes}
    finish_times = {}
    current_time = 0
    queue = deque(pid for pid, _ in processes)

    while queue:
        pid = queue.popleft()
        wait_times[pid] += current_time - last_run_time[pid]
        time_to_run = min(quantum, remaining[pid])
        print(f"[Time {current_time:02d}] Process {pid} runs for {time_to_run} units.")
        current_time += time_to_run
        remaining[pid] -= time_to_run
        last_run_time[pid] = current_time
        if remaining[pid] > 0:
            queue.append(pid)
        else:
            finish_times[pid] = current_time
            print(f"[Time {current_time:02d}] Process {pid} finishes.")

    count = len(processes)
    print(f">> Round Robin Average Waiting Time: {sum(wait_times.values()) / count:.2f}")
    print(f">> Round Robin Average Turnaround Time: {sum(finish_times.values()) / count:.2f}")


def main():
    os_ready_queue = [("P1", 10), ("P2", 2), ("P3", 3)]
    simulate_fcfs(os_ready_queue)
    simulate_round_robin(os_ready_queue, quantum=3)


if __name__ == "__main__":
    main()
