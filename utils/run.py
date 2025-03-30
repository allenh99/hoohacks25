from dotenv import load_dotenv
load_dotenv()

from .chatbot_helper import *
from .search_links import *
from .scraper import *
from .rag import *

def main(claim, weight='medium'):
    if weight == 'medium':
        num_queries, num_links, num_sources, selenium_flag, rag = 4, 5, 3, True, False
    elif weight == 'heavy':
        num_queries, num_links, num_sources, selenium_flag, rag = 6, 7, 5, True, True
    else:
        num_queries, num_links, num_sources, selenium_flag, rag = 2, 3, 3, False, False
    
    queries = generate_queries(claim, num_queries)
    queries.append(claim)

    links = set()
    for query in queries:
        for l in generate_links(query, num_links):
            links.add(l)

    verified_links = verify_sources(claim, list(links))

    s = Scraper()
    context = ''
    for r, l in verified_links[:10]:
        context += s.scrape(l, selenium_flag)

    context = context[:20000]
    if rag:
        r = RAG()
        context = r.generate_context(context, claim)[:20000]
    
    label = classify_claim(claim, context)
    sources, analysis, ratings = clean_and_analyze_sources(claim, verified_links, num_sources)
    return label, sources, analysis, ratings