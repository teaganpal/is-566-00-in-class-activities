import time
from datetime import datetime

import redis

REDIS_HOST = "redis"
REDIS_PORT = 6379
INTERVAL_SECONDS = 3

def log(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [worker] {msg}", flush=True)

def main():
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
    )

    log("Worker started")
    log("Incrementing 'worker_ticks' in Redis every "
        f"{INTERVAL_SECONDS} seconds")

    while True:
        try:
            log("Doing work...")
            new_val = r.incr("worker_ticks")
            log(f"Work complete | worker_ticks={new_val}")
        except Exception as e:
            log(f"ERROR talking to Redis: {e}")

        log("Sleeping...")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()