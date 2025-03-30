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
    label,sources,analysis,ratings = run.main(textdata)
    response = {
        "label": label,
        "sources":sources,
        "analysis": analysis,
        "ratings":ratings
    }
    #print(response)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)