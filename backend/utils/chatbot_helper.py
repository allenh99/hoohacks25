from .chatbot import Chatbot

def generate_queries(query):
    c = Chatbot()
    CONTEXT = f'You are an LLM that helps a user find more information about a certain topic.'
    PROMPT = f'Generate me ten queries that I could search to find some more information about this query: {query}. For example, given the query: \"Rivian made more profit than Apple last year\", output:\n1. Rivian\' profit last year\n2. Apple profit last year\n\n Follow the format in the example, and do not provide commentary.'

    response = c.response(PROMPT, CONTEXT)
    return response