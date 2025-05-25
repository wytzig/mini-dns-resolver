# Mini DNS resolver

This repository holds a couple different services that together make a mini dns resolver. 

## Overview
```mermaid
graph TD
    A[Client App] -->|1: HTTP GET /resolve?domain=example.com| B[TLD Server]
    B -->|2: Forwards request based on TLD| C[Authoritative Server ]
    C -->|4: Returns resolved IP e.g. 192.168.1.10| B
    B -->|5: Sends IP response back to client| A

    %% Optional MongoDB integration
    C -.->|3: Reads/writes domain records| D[MongoDB]
    %% B -.->|Optional: caches results| D
```

## Setup
In order to run the projects:
1. Clone the project
1. Open one of the server's in a dedicated terminal

### option 1: run a single project (development)
1. Do a poetry install in this folder to create your venv
1. Switch to the venv and run the app.py

### option 2: run them all quickly (devops)
1. Go each of the folders
1. Run `poetry install`
1. Run `poetry run python app.py` 

1. Once you have all three services running, you can use the system by interacting with the client (so go to that application window in your terminal)
1. You should be able to resolve 'example.com' and 'test.com'