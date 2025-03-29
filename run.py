import os
from dotenv import load_dotenv
load_dotenv()

from utils.chatbot_helper import *
from utils.search_links import *
from utils.scraper import *

def main(claim):
    queries = generate_queries(claim)

    links = set()
    for query in queries:
        for l in search_urls(query):
            links.add(l)

    s = Scraper()
    context = ''
    for l in links:
        context += s.scrape(l)
    context = context[:10000]
    
    label = classify_claim(claim, context)
    return label, links