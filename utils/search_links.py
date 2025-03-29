from duckduckgo_search import DDGS

def search_urls(query):
    results = DDGS().text(query, max_results=3)
    urls = []
    for r in results:
        urls.append(r['href'])
    return urls