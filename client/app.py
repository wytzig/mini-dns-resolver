import requests
import sys
import os
import uuid
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.logger import setup_logger

logger = setup_logger()
client_id = str(uuid.uuid4())

def main():
    logger.info({
        "event": "client_started",
        "client_id": client_id,
        "severity": "INFO",
        "message": "DNS client started"
    })

    print("Simple DNS Client started. Type a domain to resolve or 'exit' to quit.")

    while True:
        domain = input("Enter domain: ").strip()
        if domain.lower() == 'exit':
            logger.info({
                "event": "client_exit",
                "client_id": client_id,
                "severity": "INFO",
                "message": "DNS client exited by user"
            })
            print("Exiting client.")
            break

        if not domain:
            continue

        start = time.time()
        try:
            response = requests.get("http://localhost:8001/resolve", params={"domain": domain}, timeout=5)
            duration_ms = int((time.time() - start) * 1000)
            response.raise_for_status()
            data = response.json()

            if "ip" in data:
                logger.info({
                    "event": "resolution_success",
                    "client_id": client_id,
                    "domain": domain,
                    "ip": data["ip"],
                    "response_time_ms": duration_ms,
                    "severity": "INFO",
                    "message": f"Resolved {domain} to {data['ip']}"
                })
                print(f"Resolved IP: {data['ip']}")
            else:
                logger.warning({
                    "event": "resolution_failed",
                    "client_id": client_id,
                    "domain": domain,
                    "response_time_ms": duration_ms,
                    "severity": "WARNING",
                    "message": f"No IP found in response: {data}"
                })
                print(f"Error: {data.get('error', 'Unknown error')}")

        except requests.RequestException as e:
            logger.error({
                "event": "request_exception",
                "client_id": client_id,
                "domain": domain,
                "severity": "ERROR",
                "message": f"Request failed: {str(e)}"
            })
            print(f"Request failed: {e}")

if __name__ == "__main__":
    main()
