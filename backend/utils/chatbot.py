import os
from openai import OpenAI

class Chatbot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("PERPLEXITY_API_KEY"),
            base_url=os.getenv("PERPLEXITY_API_ENDPOINT"),
        )

    def response(self, prompt, context=''):
        response = self.client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", 'content': context},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content.strip()