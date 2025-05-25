# load_generator.py

import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── CONFIG ─────────────────────────────────────────────────────────────────

# Target endpoint (your TLD server)
TARGET_URL = "http://localhost:8001/resolve"

# Domain pool: valid, invalid, unknown
DOMAINS = [
    "example.com",
    "test.com",
    "mywebsite.net",
    "openai.com",
    "doesnotexist.xyz",
    "invalid_domain",
    "",  # will trigger malformed‐domain path
]

TOTAL_REQUESTS = 25000       # total requests to fire
CONCURRENCY    = 50         # how many threads
MIN_DELAY      = 0.01       # min delay between requests per thread
MAX_DELAY      = 0.1        # max delay between requests per thread

# ─── WORKER ─────────────────────────────────────────────────────────────────

def worker(task_id):
    """
    Sends a single request, returns (task_id, status, elapsed_ms, domain).
    """
    domain = random.choice(DOMAINS)
    params = {"domain": domain} if domain else {}
    start = time.time()
    try:
        r = requests.get(TARGET_URL, params=params, timeout=3)
        status = r.status_code
    except Exception as e:
        status = None  # network error or timeout
    elapsed_ms = int((time.time() - start) * 1000)
    # slight random pause to spread the load
    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
    return task_id, status, elapsed_ms, domain

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print(f"Starting load test: {TOTAL_REQUESTS} requests @ x{CONCURRENCY} concurrency")
    start_time = time.time()

    results = []
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as exe:
        futures = {exe.submit(worker, i): i for i in range(TOTAL_REQUESTS)}
        for fut in as_completed(futures):
            task_id, status, elapsed_ms, domain = fut.result()
            results.append((status, elapsed_ms))
            # optional: print progress every 500 completed
            if len(results) % 500 == 0:
                print(f"  • {len(results)}/{TOTAL_REQUESTS} done")

    duration = time.time() - start_time
    success = sum(1 for s, _ in results if s and 200 <= s < 300)
    errors  = TOTAL_REQUESTS - success
    avg_ms   = sum(ms for _, ms in results) / len(results)

    print("\n=== Load Test Complete ===")
    print(f"Total time: {duration:.2f}s")
    print(f"Success  : {success}")
    print(f"Errors   : {errors}")
    print(f"Avg Latency: {avg_ms:.0f} ms")

if __name__ == "__main__":
    main()
