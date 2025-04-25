"""
Language model integration for response generation.
"""

import os
from typing import List, Optional
from abc import ABC, abstractmethod
from together import Together
import openai


class LanguageModel(ABC):
    """Abstract base class for language models."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the language model."""
        pass


class TogetherAILanguageModel(LanguageModel):
    """Implementation using Together AI."""

    def __init__(self, model_name: str = "mistralai/Mistral-Small-24B-Instruct-2501", api_key: str = None):
        """
        Initialize the Together AI language model.

        Args:
            model_name: The name of the model to use.
            api_key: Together AI API key. If not provided, defaults to TOGETHER_API_KEY env variable.
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")

        if not self.api_key:
            raise ValueError("Please provide a Together AI API key or set the TOGETHER_API_KEY environment variable.")
        
        self.client = Together(api_key=self.api_key)

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1000,
                 stop_sequences: Optional[List[str]] = None) -> str:
        """
        Generate a response using the Together AI model.

        Args:
            prompt: Input prompt for the model.
            temperature: Controls randomness (lower = more deterministic).
            max_tokens: Max tokens to generate.
            stop_sequences: Optional list of strings to stop generation.

        Returns:
            The generated response.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop_sequences
        )
        return response.choices[0].message.content


class OpenAILanguageModel(LanguageModel):
    """Implementation using OpenAI's GPT models."""

    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: str = None):
        """
        Initialize the OpenAI language model.

        Args:
            model_name: The name of the OpenAI model to use.
            api_key: OpenAI API key. If not provided, defaults to OPENAI_API_KEY env variable.
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("Please provide an OpenAI API key or set the OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.api_key
        self.client = openai

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1000,
                 stop_sequences: Optional[List[str]] = None) -> str:
        """
        Generate a response using the OpenAI model.

        Args:
            prompt: Input prompt for the model.
            temperature: Controls randomness.
            max_tokens: Max tokens to generate.
            stop_sequences: Optional list of strings to stop generation.

        Returns:
            The generated response.
        """
        response = self.client.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop_sequences
        )
        return response["choices"][0]["message"]["content"]


class LanguageModelFactory:
    """Factory for creating language model instances."""

    @staticmethod
    def get_language_model(model_type: str = "together", **kwargs) -> LanguageModel:
        """
        Return a language model instance based on model_type.

        Args:
            model_type: Type of model to use ('together', 'openai', etc.)
            **kwargs: Additional configuration for the model.

        Returns:
            A LanguageModel instance.

        Raises:
            ValueError: If model_type is unsupported.
        """
        if model_type == "together":
            return TogetherAILanguageModel(**kwargs)
        elif model_type == "openai":
            return OpenAILanguageModel(**kwargs)
        else:
            raise ValueError(f"Unsupported language model type: {model_type}")
