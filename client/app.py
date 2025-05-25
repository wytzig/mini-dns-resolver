import requests

def main():
    print("Simple DNS Client started. Type a domain to resolve or 'exit' to quit.")
    while True:
        domain = input("Enter domain: ").strip()
        if domain.lower() == 'exit':
            print("Exiting client.")
            break
        if not domain:
            continue

        try:
            response = requests.get(f"http://localhost:8001/resolve", params={"domain": domain}, timeout=5)
            response.raise_for_status()
            data = response.json()
            if "ip" in data:
                print(f"Resolved IP: {data['ip']}")
            else:
                print(f"Error: {data.get('error', 'Unknown error')}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    main()
