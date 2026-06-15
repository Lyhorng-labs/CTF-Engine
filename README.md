# Secure Python CTF Engine
**Built for the CS4Everyone: Build with Python Hackathon**

An interactive application-security platform that executes and grades untrusted Python code in real time. Instead of multiple-choice questions, users write actual Python exploits or patches to capture the flag.

## What it does
This engine provides a web-based coding lab where users submit Python code to solve specific challenges. The backend runs the code in a restricted subprocess, compares the output against the expected flag, and uses AST-based static filtering to block common malicious payloads (imports, `eval`/`exec`/`open`, etc.).

## Architecture & Technologies
This project was built from scratch without relying on container-based isolation like Docker.

* **Frontend:** Vanilla HTML, CSS, and JavaScript (zero dependencies).
* **Backend:** FastAPI (Python) for async routing and REST API generation.
* **Database:** SQLite with SQLModel/SQLAlchemy for relational storage and leaderboard queries.
* **Security layer:** Custom Abstract Syntax Tree (AST) static analyzer plus an isolated Python subprocess with a hard timeout.

## Security Model (The Sandbox)

Executing untrusted code is inherently dangerous, so the engine applies two layers of defense before and during execution:

1. **AST allowlist:** Before any code runs, the engine parses the raw string into an Abstract Syntax Tree (`ast`) and enforces an allowlist of modules (`math`, `hashlib`, `datetime`, `json`, `random`). It blocks both direct (`import os`) and `from`-style (`from subprocess import run`) imports, and rejects `__import__`, `eval`, `exec`, and `open`.
2. **Subprocess + hard timeout:** Approved code runs in a separate Python process (`python -c`). If a user submits an infinite loop (`while True:`), the process is terminated after 2 seconds to prevent simple DoS via long-running code.

> **Note:** This is a code filter plus a timeout, not a full sandbox. The code still runs on the same machine, so a skilled attacker could get around it. Stronger isolation (Docker, etc.) is planned for later.

## How to Run Locally

**1. Clone the repository and enter the directory:**
```bash
git clone https://github.com/Lyhorng-labs/CTF-Engine.git
cd CTF-Engine
```

**2. Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install fastapi uvicorn sqlmodel
```

**4. Start the backend server:**
```bash
uvicorn main:app --reload
```

**5. Open the frontend:**
Open `Interface/index.html` in your browser (the API runs at `http://127.0.0.1:8000`).
