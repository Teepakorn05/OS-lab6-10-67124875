"""Illustrate FCFS vs token-by-token service for two AI requests (Lab 7)."""
import time


class AIRequest:
    def __init__(self, user_id, tokens_required):
        self.user_id = user_id
        self.tokens_required = tokens_required
        self.tokens_generated = 0


def simulate_ai_fcfs(requests):
    print("\n[AI Server] Strategy: First-Come, First-Served")
    for req in requests:
        print(f"-> Starting {req.user_id} (Needs {req.tokens_required} tokens)...")
        time.sleep(0.05 * req.tokens_required)
        print(f"   [DONE] {req.user_id} finished.")


def simulate_ai_round_robin(requests):
    print("\n[AI Server] Strategy: Round Robin (one token per turn)")
    queue = list(requests)
    while queue:
        req = queue.pop(0)
        req.tokens_generated += 1
        print(f"   {req.user_id}: generated token {req.tokens_generated}")
        if req.tokens_generated == req.tokens_required:
            print(f"   [DONE] {req.user_id} finished early!")
        else:
            queue.append(req)
        time.sleep(0.01)


def main():
    print("--- Incoming API Requests ---")
    simulate_ai_fcfs([AIRequest("User_A_Essay", 10), AIRequest("User_B_Math", 2)])
    simulate_ai_round_robin([AIRequest("User_A_Essay", 10), AIRequest("User_B_Math", 2)])


if __name__ == "__main__":
    main()
