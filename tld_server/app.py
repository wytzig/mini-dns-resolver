from flask import Flask, request, jsonify
import requests
import sys
import os
import random
import time
from datetime import datetime
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.logger import setup_logger

app = Flask(__name__)
logger = setup_logger()

# Mapping TLD to authoritative server URLs
TLD_MAP = {
    "com": "http://localhost:8002",
    "net": "http://localhost:8003"  # Extendable
}

@app.route('/resolve')
def resolve():
    domain = request.args.get('domain', '').strip()
    request_id = str(uuid.uuid4())

    if not domain or '.' not in domain:
        logger.warning({
            "request_id": request_id,
            "event": "invalid_domain_request",
            "domain": domain,
            "severity": "WARNING",
            "service": "tld_server",
            "client_ip": request.remote_addr,
            "message": "Malformed domain name"
        })
        return jsonify({"error": "Invalid domain"}), 400

    tld = domain.split('.')[-1]
    auth_server_url = TLD_MAP.get(tld)
    if not auth_server_url:
        logger.warning({
            "request_id": request_id,
            "event": "unsupported_tld",
            "domain": domain,
            "tld": tld,
            "severity": "WARNING",
            "service": "tld_server",
            "client_ip": request.remote_addr,
            "message": f"TLD '{tld}' not supported"
        })
        return jsonify({"error": f"TLD '{tld}' not supported"}), 404

    try:
        start_time = time.time()
        resp = requests.get(f"{auth_server_url}/resolve", params={"domain": domain}, timeout=5)
        duration_ms = int((time.time() - start_time) * 1000)
        resp.raise_for_status()

        logger.info({
            "request_id": request_id,
            "event": "domain_forwarded",
            "domain": domain,
            "tld": tld,
            "auth_server": auth_server_url,
            "status": resp.status_code,
            "duration_ms": duration_ms,
            "severity": "INFO",
            "service": "tld_server",
            "client_ip": request.remote_addr,
            "message": "Domain resolution forwarded successfully"
        })
        return jsonify(resp.json())
    
    except requests.RequestException as e:
        logger.error({
            "request_id": request_id,
            "event": "auth_server_error",
            "domain": domain,
            "tld": tld,
            "auth_server": auth_server_url,
            "severity": "ERROR",
            "service": "tld_server",
            "client_ip": request.remote_addr,
            "message": f"Failed to contact authoritative server: {str(e)}"
        })
        return jsonify({"error": f"Failed to contact authoritative server: {e}"}), 502

def simulate_success_requests(n=10, delay_range=(0.2, 1.0)):
    """Simulates a batch of requests for testing logging."""
    test_domains = ["example.com", "openai.com", "test.com", "mywebsite.net"]
    for _ in range(n):
        domain = random.choice(test_domains)
        try:
            logger.debug({
                "event": "simulation_start",
                "domain": domain,
                "service": "tld_server",
                "severity": "DEBUG",
                "message": f"Simulating resolution for {domain}"
            })
            requests.get("http://localhost:8001/resolve", params={"domain": domain})
        except Exception as e:
            logger.error({
                "event": "simulation_request_failed",
                "domain": domain,
                "service": "tld_server",
                "severity": "ERROR",
                "message": str(e)
            })
        time.sleep(random.uniform(*delay_range))

def main():
    # Optionally simulate traffic when server starts
    if os.environ.get("SIMULATE_TRAFFIC") == "1":
        simulate_success_requests(n=50)

    logger.info({
        "event": "tld_server_started",
        "severity": "INFO",
        "service": "tld_server",
        "message": "TLD Server is now running"
    })

    app.run(host="0.0.0.0", port=8001)

if __name__ == "__main__":
    main()
