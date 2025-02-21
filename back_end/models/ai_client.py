from openai import Client as OpenAI
from typing import TypeVar, Generic
import requests

T = TypeVar('T')

class Ai():
    def __init__(self):
        # Check if ollama is running
        check = requests.get('http://ollama:11434')
        if check.status_code == 200:
            self.client = OpenAI(
                base_url = 'http://ollama:11434/v1',
                api_key='ollama', # required, but unused
            )
            self.default_model = "deepseek-r1:14b"
        else:
            self.client = OpenAI()
            self.default_model = "gpt-4o-2024-08-06"

    def complete(self, messages, model = None,**kwargs):
        response = self.client.chat.completions.create(
            model=model if model else self.default_model,
            messages=messages,
            **kwargs  # Pass additional options as keyword arguments
        )
        return response.choices[0].message.content


    def structured_complete(self, messages, structure: T, model=None, **kwargs) -> T:
        completion = self.client.beta.chat.completions.parse(
            model=model if model else self.default_model,
            messages=messages,
            response_format=structure,
            **kwargs  # Pass additional options as keyword arguments
        )
        return completion.choices[0].message.parsed




