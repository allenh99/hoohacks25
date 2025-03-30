import os
from openai import OpenAI

class Chatbot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("PERPLEXITY_API_KEY"),
            base_url=os.getenv("PERPLEXITY_API_ENDPOINT"),
        )

    def response(self, prompt, context='', sources=False):
        response = self.client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", 'content': context},
                {"role": "user", "content": prompt}
            ],
        )
        if sources:
            return response.choices[0].message.content.strip(), response.citations
        return response.choices[0].message.content.strip()