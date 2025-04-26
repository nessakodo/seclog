# SecLog Watch 

A lightweight security log monitoring tool with real-time dashboard.

- Backend: Python + Watchdog
- Frontend: HTML/CSS/JavaScript (deployed on GitHub Pages)

## Live Dashboard
[View SecLog Dashboard here!](https://nessakodo.github.com/seclog-watch/)

## How to Run Locally

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/seclog-watch.git
    cd seclog-watch
    ```

2. Run the backend log monitor:
    ```bash
    python backend/watcher.py
    ```

3. In a new terminal, serve the frontend:
    ```bash
    cd frontend
    python3 -m http.server 8000
    ```

4. Visit [http://localhost:8000](http://localhost:8000) in your browser.

---


## Tech Stack

- Python (backend monitoring)
- HTML/CSS/JS (frontend dashboard)
- GitHub Pages (hosting)

---

## Features

- Real-time suspicious log detection
- Live updating dashboard
- Mobile-responsive hacker-style UI
- Sleek green-on-black cyber theme