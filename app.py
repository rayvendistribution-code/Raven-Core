from raven import Raven
from flask import Flask, request, jsonify

app = Flask(__name__)
raven = Raven()

@app.route('/chat', methods= )
def chat():
    data = request.json
    message = data.get('message', '')
    # We'll hook your actual response logic here later
    return jsonify({"response": f"Raven heard you say: {message}"})

if __name__ == '__main__':
    app.run(debug=True)