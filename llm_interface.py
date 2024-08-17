from abc import ABC, abstractmethod
from openai import OpenAI
import anthropic
import json
import requests


class LLMProvider(ABC):
    @abstractmethod
    def analyze(self, query: str, context: str) -> str | None:
        pass


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def analyze(self, query, context):
        prompt = f"""
        Analyze the following social security data and provide insights:
        {context}

        Please provide:
        1. A summary of the data
        2. Key trends or patterns
        3. Recommendations based on the analysis
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes social security data.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)

    def analyze(self, query, context):
        prompt = f"""
        Analyze the following social security data and provide insights:
        {context}

        Please provide:
        1. A summary of the data
        2. Key trends or patterns
        3. Recommendations based on the analysis
        """

        response = self.client.completions.create(
            model="claude-3-sonnet-20240229",
            prompt=prompt,
            max_tokens=1000,
        )

        return response.completion


class OllamaProvider(LLMProvider):
    def __init__(self, model="llama3.1"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def analyze(self, query, context):
        prompt = f"""
        Given the following context about social security data:
        {context}

        Please analyze this data to answer the following query:
        {query}

        Provide a detailed response including:
        1. A summary of the relevant data
        2. Key insights or patterns related to the query
        3. Recommendations or conclusions based on the analysis
        """

        payload = {"model": self.model, "prompt": prompt, "stream": False}

        response = requests.post(self.api_url, json=payload)
        if response.status_code == 200:
            return json.loads(response.text)["response"]
        else:
            raise Exception(f"Error from Ollama API: {response.text}")
