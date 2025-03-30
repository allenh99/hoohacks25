from duckduckgo_search import DDGS

def search_urls(query):
    print(query)
    results = DDGS().text(query, max_results=5)
    urls = []
    for r in results:
        urls.append(r['href'])
    return urls