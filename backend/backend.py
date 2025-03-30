from flask import Flask, request, jsonify
from utils import run

app = Flask(__name__)

@app.route('/api/analyze/', methods=['POST'])
def analyze():
    #print(request)
    if not request.is_json:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    
    data = request.get_json()
    textdata,weight = data['text'],data['weight']
    if textdata is None:
        return jsonify({"error": "Missing 'text' field"})
    #label,sources,analysis,ratings = run.main(textdata,weight)
    label,sources,analysis,ratings = ('Incorrect', ['https://www.whitehouse.gov/briefings-statements/2025/01/press-briefing-by-press-secretary-karoline-leavitt/', 'https://www.presidency.ucsb.edu/statistics/elections/2024', 'https://www.britannica.com/biography/Joe-Biden'], ["The link [https://www.whitehouse.gov/briefings-statements/2025/01/press-briefing-by-press-secretary-karoline-leavitt/](https://www.whitehouse.gov/briefings-statements/2025/01/press-briefing-by-press-secretary-karoline-leavitt/) provides information about a press briefing by Karoline Leavitt, who is acting as the Press Secretary for the White House, specifically during a time when it mentions President Trump's activities and strategies. This is relevant to the query about Joe Biden being the current president of the U.S. because it indicates a change in administration, as Karoline Leavitt is mentioned in the context of a Trump administration, whereas Joe Biden was the predecessor. Thus, this link indirectly suggests that there might have been a transition, offering some background on why Joe Biden might not be the current president. Additionally, it discusses changes in White House policies and media interactions under a new administration, which could be part of broader discussions about presidential transitions and changes in leadership roles.", 'The link https://www.presidency.ucsb.edu/statistics/elections/2024 provides information on the 2024 U.S. presidential election statistics, which could be relevant in discussing the current president of the United States. This source might offer details such as election results, voting trends, and changes in leadership that could help clarify whether Joe Biden remains the president. Specifically, it could provide data on who won the election, electoral and popular vote margins, and any shifts in party control, all of which are crucial in determining the current presidential status.', 'The provided link, [https://www.britannica.com/biography/Joe-Biden](https://www.britannica.com/biography/Joe-Biden), is relevant for discussing the query "Joe Biden is the current president of the US." because it provides comprehensive information about Joe Biden\'s career and tenure in public office. Specifically, it states that Joe Biden served as the 46th president of the United States from 2021 to 2025, making him the current president during that period but not at present[3]. This link offers background on his political journey, including his time as U.S. Senator and Vice President, which can help contextualize his presidency and clarify that he is not the current president beyond 2025.'], [9, 9, 9])

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