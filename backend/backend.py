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
    #label,sources,analysis,ratings = ('Incorrect', ['https://www.whitehouse.gov/briefings-statements/2025/01/press-briefing-by-press-secretary-karoline-leavitt/', 'https://www.presidency.ucsb.edu/statistics/elections/2024', 'https://www.britannica.com/biography/Joe-Biden'], ["The link [https://www.whitehouse.gov/briefings-statements/2025/01/press-briefing-by-press-secretary-karoline-leavitt/](https://www.whitehouse.gov/briefings-statements/2025/01/press-briefing-by-press-secretary-karoline-leavitt/) provides information about a press briefing by Karoline Leavitt, who is acting as the Press Secretary for the White House, specifically during a time when it mentions President Trump's activities and strategies. This is relevant to the query about Joe Biden being the current president of the U.S. because it indicates a change in administration, as Karoline Leavitt is mentioned in the context of a Trump administration, whereas Joe Biden was the predecessor. Thus, this link indirectly suggests that there might have been a transition, offering some background on why Joe Biden might not be the current president. Additionally, it discusses changes in White House policies and media interactions under a new administration, which could be part of broader discussions about presidential transitions and changes in leadership roles.", 'The link https://www.presidency.ucsb.edu/statistics/elections/2024 provides information on the 2024 U.S. presidential election statistics, which could be relevant in discussing the current president of the United States. This source might offer details such as election results, voting trends, and changes in leadership that could help clarify whether Joe Biden remains the president. Specifically, it could provide data on who won the election, electoral and popular vote margins, and any shifts in party control, all of which are crucial in determining the current presidential status.', 'The provided link, [https://www.britannica.com/biography/Joe-Biden](https://www.britannica.com/biography/Joe-Biden), is relevant for discussing the query "Joe Biden is the current president of the US." because it provides comprehensive information about Joe Biden\'s career and tenure in public office. Specifically, it states that Joe Biden served as the 46th president of the United States from 2021 to 2025, making him the current president during that period but not at present[3]. This link offers background on his political journey, including his time as U.S. Senator and Vice President, which can help contextualize his presidency and clarify that he is not the current president beyond 2025.'], [9, 9, 9])
    label,sources,analysis,ratings = ('Incorrect', ['https://en.wikipedia.org/wiki/Wealth_of_Elon_Musk', 'https://people.com/what-is-elon-musk-net-worth-11696472', 'https://economictimes.com/news/international/global-trends/gap-between-elon-musks-net-worth-and-worlds-next-richest-jeff-bezos-237-billion-will-leave-you-stunned/articleshow/116918751.cms'], ['Analysis: The link provided describes the wealth of Elon Musk, noting his rise to becoming one of the wealthiest individuals globally with a net worth exceeding $300 billion as of early 2025, but it does not mention him earning a trillion dollars in 2024. Instead, Elon Musk became the first person to reach a net worth of over $400 billion in December 2024, primarily due to his stakes in Tesla and SpaceX[3].', "Analysis: The article from People.com does not support the claim that Elon Musk earned a trillion dollars in 2024. Instead, it reports that Musk's net worth surpassed $400 billion in December 2024, but subsequently declined to approximately $330 billion by March 2025 due to fluctuations in Tesla's stock prices and other factors[1].", "Analysis: The article discusses the significant gap between Elon Musk's net worth and that of Jeff Bezos, but it does not support the claim that Elon Musk earned a trillion dollars in 2024. Instead, it highlights a substantial increase in Musk's wealth, reaching over $442 billion, driven by factors like Tesla's stock performance and his political connections, yet this figure remains below $1 trillion[2]."], [9, 8, 7])
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