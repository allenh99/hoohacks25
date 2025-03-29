import os
from dotenv import load_dotenv
load_dotenv()

from .chatbot_helper import *
from .search_links import *
from .scraper import *
from .rag import *

def main(claim, rag=False):
    queries = generate_queries(claim)

    links = set()
    for query in queries:
        for l in search_urls(query):
            links.add(l)

    s = Scraper()
    context = ''
    for l in links:
        context += s.scrape(l)

    r = RAG()

    context = context[:50000]
    if rag:
        context = r.generate_context(context, claim)
    
    label = classify_claim(claim, context)
    return label, list(links)