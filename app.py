from flask import Flask, request, jsonify
from raven import Raven

app = Flask(__name__)
raven = Raven()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    return jsonify({"response": f"Raven heard you say: {message}"})

if __name__ == "__main__":
    app.run(debug=True)
