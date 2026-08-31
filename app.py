from flask import Flask, request, jsonify, render_template
from raven import Raven

app = Flask(__name__)
raven = Raven()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    message = (data.get("message") or "").strip()
    reply = raven.respond(message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
