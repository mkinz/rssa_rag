from abc import ABC, abstractmethod
from openai import OpenAI
import anthropic
import json
import requests
from dotenv import load_dotenv
import os
from typing import Any


class LLMProvider(ABC):
    @abstractmethod
    def analyze(self, query: str, context: str) -> str | None | Any:
        pass


class OpenAIProvider(LLMProvider):
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

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
    def __init__(self):
        load_dotenv()
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def analyze(self, query, context):
        prompt = f"""
        Analyze the following social security data and provide insights:
        {context}

        Please provide:
        1. A summary of the data
        2. Key trends or patterns
        3. Recommendations based on the analysis
        """

        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0,
            system="You are a helpful assistant that analyzes social security data.",
            messages=[{"role": "user", "content": prompt}],
        )

        if response.content and len(response.content) > 0:
            return response.content[0].text
        else:
            return "No content found in response"


class OllamaProvider(LLMProvider):
    """
    Note: Ollama server must be running locally before this will work.
    commands: ollama serve
    """

    def __init__(self, model="mistral-nemo"):
        # def __init__(self, model="gemma2:9b"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"
        print(f"using {self.model}")

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
