import random
import time
import sys

# Tune these probabilities to make chaos rare but impactful
CHAOS_CONFIG = {
    "crash_probability": 0.05,         # 5% chance the service dies
    "timeout_probability": 0.1,        # 10% chance of delay
    "bad_response_probability": 0.07,  # 7% chance of invalid/malicious response
    "empty_result_probability": 0.1    # 10% chance of 'no result' despite correct input
}

def maybe_crash():
    if random.random() < CHAOS_CONFIG["crash_probability"]:
        print("💥 Chaos: Simulating server crash!")
        sys.exit(1)

def maybe_timeout():
    if random.random() < CHAOS_CONFIG["timeout_probability"]:
        delay = random.uniform(3, 7)
        print(f"🐢 Chaos: Delaying response by {delay:.2f} seconds.")
        time.sleep(delay)

def maybe_return_bad_response():
    return random.random() < CHAOS_CONFIG["bad_response_probability"]

def maybe_empty_result():
    return random.random() < CHAOS_CONFIG["empty_result_probability"]
