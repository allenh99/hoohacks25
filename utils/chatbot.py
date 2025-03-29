import os
from openai import AzureOpenAI

class Chatbot:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT")
        )

    def response(self, prompt, context=''):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", 'content': context},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content.strip()