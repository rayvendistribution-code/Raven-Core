# Base44 Dev Environment

## What this is
A small Python/Flask chatbot ("Raven"). The canonical web entry is the Flask app in `app.py`, run via gunicorn (per `Procfile`).

## Stack
- Python 3.11 (`runtime.txt`), Flask + gunicorn (`requirements.txt`)
- `main.py` is a FastAPI alternative that is NOT in requirements (no fastapi/uvicorn installed) — not the run entry.
- `raven.py` defines the `Raven` class and prints status banners on import; both entry points import it.

## Run
```
docker compose -f docker-compose.base44.yml up -d
```
- Serves on host port 3000 (gunicorn bound to 0.0.0.0:8000 inside, mapped 3000:8000).
- `--reload` is on, so edits to source hot-reload without a rebuild.
- Dependencies install on container start via `pip install -r requirements.txt`.

## Verify
- `curl http://localhost:3000/` → JSON status
- `curl -X POST http://localhost:3000/chat -H 'Content-Type: application/json' -d '{"message":"hi"}'` → echo response

## Secrets
None required — no external services.
