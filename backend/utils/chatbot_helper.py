import re
from .chatbot import Chatbot

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
    for r in response.split('\n'):
        if r: links.append(r)
    return links

def verify_sources(claim, urls):
    c = Chatbot()
    CONTEXT = f'You are an LLM that helps verify the legitimacy of certain sources.'
    PROMPT = f'Given the following urls: {', '.join(urls)}, rank them based on their legitimacy and relevance on a scale of 1 to 10 on the following claim: {claim}. Please put the ratings in the format:\n**Legitimacy: 8**\n**Relevance: 9**\n\n Make sure to rate every link provided.'

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
                relevance_ratings.append(int(r.split(':')[1].replace('*', '').strip()))
            else:
                retrieved_urls.append(r)

    sorted_sources = []
    for i in range(len(retrieved_urls)):
        sorted_sources.append(((legitimacy_ratings[i] + relevance_ratings[i]) // 2, retrieved_urls[i]))
    sorted_sources = sorted(sorted_sources)[::-1]
    return sorted_sources

def classify_claim(query, context):
    c = Chatbot()
    CONTEXT = f'You are an LLM that helps figure out if a claim is false or not given some context.'
    PROMPT = f'Given the following context: \n\n {context} \n\n Is the following claim correct: {query}? Output \'Correct\' or \'Incorrect\', do not provide any commentary.'

    response = c.response(PROMPT, CONTEXT)
    return response

def clean_and_analyze_sources(query, urls, top_depth):
    top_sources, top_ratings, top_analysis = [], [], []
    seen_base = set()
    for rating, url in urls:
        if len(top_sources) >= top_depth: break
        url_base = url.split('//')[1].split('/')[0]
        if url_base not in seen_base:
            seen_base.add(url_base)
            top_sources.append(url)
            top_ratings.append(rating)
    
    c = Chatbot()
    CONTEXT = f'You are an LLM analyzes a link and creates a summary for how the link might help provide more information on a query.'
    for url in top_sources:
        PROMPT = f'What information could the following link: {url} \n provide in discussing the following query: {query}? Only point out how the source is relevant, omit any negative details about the source.'
        response = c.response(PROMPT, CONTEXT)
        top_analysis.append(response)
    
    return top_sources, top_analysis, top_ratings
