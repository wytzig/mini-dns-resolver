from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mapping TLD to authoritative server URLs (could be read from a config file, volume mapped)
TLD_MAP = {
    "com": "http://localhost:8002",
    "net": "http://localhost:8003"  # Optional for extension
}

@app.route('/resolve')
def resolve():
    domain = request.args.get('domain', '').strip()
    if not domain or '.' not in domain:
        return jsonify({"error": "Invalid domain"}), 400

    tld = domain.split('.')[-1]
    auth_server_url = TLD_MAP.get(tld)
    if not auth_server_url:
        return jsonify({"error": f"TLD '{tld}' not supported"}), 404

    try:
        resp = requests.get(f"{auth_server_url}/resolve", params={"domain": domain}, timeout=5)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to contact authoritative server: {e}"}), 502

def main():
    app.run(host="0.0.0.0", port=8001)

if __name__ == "__main__":
    main()
