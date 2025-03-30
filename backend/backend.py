from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/analyze/', methods=['POST'])
def analyze():
    if not request.is_json:
        return jsonify({"error": "Invalid input, expected JSON"}), 400

    data = request.get_json()
    print(data)
    response = {
        "message": "Data received successfully",
        "received_data": data,
        "status": "processed"
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)