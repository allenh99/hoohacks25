from flask import Flask, request, jsonify
from utils import run

app = Flask(__name__)

@app.route('/api/analyze/', methods=['POST'])
def analyze():
    #print(request)
    if not request.is_json:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    
    data = request.get_json()
    textdata = data['text']
    if textdata is None:
        return jsonify({"error": "Missing 'text' field"})
    label,links = run.main(textdata)
    response = {
        "response": label,
        "links": links
    }
    #print(response)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)