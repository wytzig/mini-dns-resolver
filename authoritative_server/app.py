from flask import Flask, request, jsonify

app = Flask(__name__)

# Domain to IP mapping (could be volume mapped or read from file)
DOMAIN_IP_MAP = {
    "example.com": "192.168.1.10",
    "test.com": "192.168.1.11"
}

@app.route('/resolve')
def resolve():
    domain = request.args.get('domain', '').strip()
    if not domain:
        return jsonify({"error": "No domain provided"}), 400

    ip = DOMAIN_IP_MAP.get(domain)
    if ip:
        return jsonify({"ip": ip})
    else:
        return jsonify({"error": f"Domain '{domain}' not found"}), 404

def main():
    app.run(host="0.0.0.0", port=8002)

if __name__ == "__main__":
    main()
