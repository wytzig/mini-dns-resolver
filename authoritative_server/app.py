from flask import Flask, request, jsonify
import sys
import os
import uuid
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.chaos import maybe_crash, maybe_timeout, maybe_return_bad_response, maybe_empty_result
from common.logger import setup_logger

app = Flask(__name__)
logger = setup_logger()

# Unique ID to trace which auth server this is (if you run multiple)
AUTH_SERVER_ID = os.environ.get("AUTH_SERVER_ID", str(uuid.uuid4())[:8])

# Domain to IP mapping
DOMAIN_IP_MAP = {
    "example.com": "192.168.1.10",
    "test.com": "192.168.1.11"
}
@app.route('/resolve')
def resolve():
    maybe_crash()
    maybe_timeout()

    domain = request.args.get('domain', '').strip()
    request_id = str(uuid.uuid4())

    if not domain:
        logger.warning({
            "event": "missing_domain",
            "severity": "WARNING",
            "request_id": request_id,
            "auth_server_id": AUTH_SERVER_ID,
            "message": "No domain provided in request"
        })
        return jsonify({"error": "No domain provided"}), 400

    # Bad response case
    if maybe_return_bad_response():
        logger.error({
            "event": "corrupt_response",
            "severity": "ERROR",
            "request_id": request_id,
            "auth_server_id": AUTH_SERVER_ID,
            "domain": domain,
            "message": "Returning invalid response due to chaos"
        })
        return "<<<BAD_JSON", 500

    if maybe_empty_result():
        logger.warning({
            "event": "empty_result",
            "severity": "WARNING",
            "request_id": request_id,
            "auth_server_id": AUTH_SERVER_ID,
            "domain": domain,
            "message": "Simulating domain not found"
        })
        return jsonify({"error": f"Domain '{domain}' not found"}), 404

    ip = DOMAIN_IP_MAP.get(domain)
    if ip:
        logger.info({
            "event": "resolution_success",
            "severity": "INFO",
            "request_id": request_id,
            "auth_server_id": AUTH_SERVER_ID,
            "domain": domain,
            "ip": ip,
            "message": f"Domain '{domain}' resolved to {ip}"
        })
        return jsonify({"ip": ip})
    else:
        logger.warning({
            "event": "domain_not_found",
            "severity": "WARNING",
            "request_id": request_id,
            "auth_server_id": AUTH_SERVER_ID,
            "domain": domain,
            "message": f"Domain '{domain}' not found in mapping"
        })
        return jsonify({"error": f"Domain '{domain}' not found"}), 404


def main():
    logger.info({
        "event": "auth_server_started",
        "severity": "INFO",
        "auth_server_id": AUTH_SERVER_ID,
        "message": "Authoritative server started and ready to receive requests"
    })
    app.run(host="0.0.0.0", port=8002)

if __name__ == "__main__":
    main()
