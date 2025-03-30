from dotenv import load_dotenv
load_dotenv()

from .chatbot_helper import *
from .search_links import *
from .scraper import *
from .rag import *

def main(claim, rag=False):
    queries = generate_queries(claim)
    queries.append(claim)

    links = set()
    for query in queries:
        time.sleep(1)
        for l in generate_links(query):
            links.add(l)
    print(links)

    verified_links = verify_sources(claim, list(links))

    s = Scraper()
    context = ''
    for r, l in verified_links[:10]:
        context += s.scrape(l)

    context = context[:50000]
    if rag:
        r = RAG()
        context = r.generate_context(context, claim)
    
    label = classify_claim(claim, context)
    sources, analysis, ratings = clean_and_analyze_sources(claim, verified_links)
    return label, sources, analysis, ratings