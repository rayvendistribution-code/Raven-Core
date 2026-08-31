import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

from flask import Flask, jsonify, render_template, request

from raven import Raven

app = Flask(__name__)
raven = Raven()


def supabase_request(path: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None) -> bool:
    supabase_url = os.environ.get("SUPABASE_URL")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not supabase_url or not service_key:
        return False

    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request_url = f"{supabase_url}/rest/v1/{path}"
    db_request = urllib.request.Request(
        request_url,
        data=body,
        method=method,
        headers={
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )
    try:
        with urllib.request.urlopen(db_request, timeout=3) as response:
            return 200 <= response.status < 300
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return False


@app.get("/")
def home() -> str:
    return render_template("index.html")


@app.post("/chat")
def chat() -> Any:
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    session_id = str(data.get("session_id", "")).strip()

    if not message:
        return jsonify({"error": "Say something first."}), 400
    if len(message) > 1200:
        return jsonify({"error": "Keep it under 1,200 characters."}), 400

    stored_user_message = False
    if session_id:
        stored_user_message = supabase_request(
            "chat_messages",
            "POST",
            {"session_id": session_id, "role": "user", "content": message},
        )

    response = raven.reply(message)
    stored_response = False
    if session_id:
        stored_response = supabase_request(
            "chat_messages",
            "POST",
            {"session_id": session_id, "role": "assistant", "content": response},
        )

    return jsonify(
        {
            "response": response,
            "persisted": stored_user_message and stored_response,
        }
    )


@app.get("/status")
def status() -> Any:
    return jsonify(
        {
            "name": raven.name,
            "status": raven.status,
            "creator": raven.creator,
            "memories": len(raven.lora_memory),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
