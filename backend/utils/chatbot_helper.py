import re
from .chatbot import Chatbot

def generate_sources(claim):
    c = Chatbot()
    CONTEXT = f'You are an assistant that helps a user fact check certain claims.'
    PROMPT = f'Fact check this: {claim}'

    response, sources = c.response(PROMPT, CONTEXT, sources=True)
    return response, sources

def classify_claim(claim, response):
    c = Chatbot()
    CONTEXT = f'You are an assistant that helps a user fact check certain claims.'
    PROMPT = f'Given this claim:\n\n{claim}\n\nand this response\n\n{response}\n\nIs the claim correct, incorrect, misleading, exaggerating, or partially correct? Only output \'Correct\', \'Incorrect\', \'Partially Correct\', \'Misleading\', or \'Exaggerating\'.'

    response = c.response(PROMPT, CONTEXT)
    return response

def clean_url(url):
    for split_r in url.replace('[', ' ').replace(']', ' ').split():
        if re.search('http', split_r, re.IGNORECASE):
            if split_r[-1] == '/':
                split_r = split_r[:-1]
            return split_r
    return ''

def generate_queries(claim, num_queries):
    c = Chatbot()
    CONTEXT = f'You are an LLM that helps a user find more information about a certain topic.'
    PROMPT = f'Generate me {num_queries} queries that I could search to find some more information to verify or disprove this claim: {claim}. For example, given the query: \"Rivian made more profit than Apple last year\", output:\n1. Rivian\' profit last year\n2. Apple profit last year\n\n Follow the format in the example, and do not provide commentary.'

    queries = []
    response = c.response(PROMPT, CONTEXT)
    for q in response.split('\n'):
        queries.append(q)
    return queries

def generate_links(query, num_links):
    c = Chatbot()
    CONTEXT = f'You are an LLM that generates links to help a user learn more about a certain topic.'
    PROMPT = f'Generate me {num_links} links that I could use to find some more information about {query}. Do not provide commentary, only the links without any bullet points.'
    
    links = []
    response = c.response(PROMPT, CONTEXT)
    for url in response.split('\n'):
        url = clean_url(url)
        if url: links.append(url)
    return links

def verify_sources(claim, urls):
    c = Chatbot()
    urls_join = '\n'.join(urls)
    CONTEXT = f'You are an LLM that helps verify the legitimacy of certain sources.'
    PROMPT = f'You are an expert researcher who is looking to answer this query: "{claim}". Given these sources as links:\n\n{urls_join}\n\nCan you rank them based on legitimacy of the source, and relevance to the query, and output a string with each link, its legitimacy, and relevance like this:\n\n**link**\n**Legitimacy: 8**\n**Relevance: 7**'

    retrieved_urls = []
    legitimacy_ratings = []
    relevance_ratings = []
    response = c.response(PROMPT, CONTEXT)
    for rating in response.split('\n\n'):
        if not re.search(r'\*\*legitimacy', rating, re.IGNORECASE): continue
        for r in rating.split('\n'):
            if re.search(r'\*\*legitimacy', r, re.IGNORECASE):
                legitimacy_ratings.append(int(r.split(':')[1].replace('*', '').strip()))
            elif re.search(r'\*\*relevance', r, re.IGNORECASE):
                relevance_ratings.append(int(r.split(':')[1].replace('*', '').split()[0].strip()))
            else:
                for split_r in r.split('**'):
                    if re.search(r'http', split_r, re.IGNORECASE):
                        retrieved_urls.append(split_r)
                        break

    sorted_sources = []
    try:
        for i in range(len(retrieved_urls)):
            sorted_sources.append(((legitimacy_ratings[i] + relevance_ratings[i]) // 2, retrieved_urls[i]))
    except:
        print(response)
        print(retrieved_urls, legitimacy_ratings, relevance_ratings)
        input()
    sorted_sources = sorted(sorted_sources)[::-1]
    return sorted_sources

def classify_claim(query, context):
    c = Chatbot()
    CONTEXT = f'You are an LLM that helps figure out if a claim is false or not given some context.'
    PROMPT = f'Given the following context:\n\n{context}\n\n Is the following claim correct: {query}? Output \'Correct\' or \'Incorrect\', do not provide any commentary.'

    response = c.response(PROMPT, CONTEXT)
    return response

def clean_and_analyze_sources(query, urls, top_depth):
    top_sources, top_ratings, top_analysis = [], [], []
    seen_base = set()
    for rating, url in urls:
        url = clean_url(url)
        if len(top_sources) >= top_depth: break
        url_base = url.split('//')[1].split('/')[0]
        if re.match('www.', url_base):
            url_base = url_base[4:]
        if url_base not in seen_base:
            seen_base.add(url_base)
            top_sources.append(url)
            top_ratings.append(rating)
    
    c = Chatbot()
    CONTEXT = f'You are an expert researcher looking into this claim: {query}'
    for url in top_sources:
        PROMPT = f'Given this source as a link:\n\n{url}\n\nCan you give a 1-2 sentence analysis about this link, like this: \n\n**Analysis: ...**'
        response = c.response(PROMPT, CONTEXT)
        top_analysis.append(response)
    
    return top_sources, top_analysis, top_ratings
