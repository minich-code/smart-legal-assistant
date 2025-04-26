
"""
Language model integration for response generation.
"""
import os
from typing import List, Optional
from abc import ABC, abstractmethod

from dotenv import load_dotenv  # <-- Important for local .env files

load_dotenv()  # <-- Automatically load .env variables when the file runs

class LanguageModel(ABC):
    """Base class for language models."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the language model."""
        pass


class TogetherAILanguageModel(LanguageModel):
    """Language model implementation using Together AI."""

    def __init__(self, model_name: str = "mistralai/Mistral-Small-24B-Instruct-2501", api_key: Optional[str] = None):
        """Initialize Together AI language model."""
        from together import Together  # Delayed import to avoid unnecessary dependency issues

        self.model_name = model_name
        self.api_key = api_key or os.getenv("TOGETHER_AI_API_KEY")

        if not self.api_key:
            raise ValueError("Please provide a Together AI API key or set the TOGETHER_AI_API_KEY environment variable.")

        self.client = Together(api_key=self.api_key)

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1000,
                 stop_sequences: Optional[List[str]] = None) -> str:
        """Generate a response from the Together AI model."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop_sequences
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error during Together AI generation: {e}")


def get_language_model(model_type: str = "together", **kwargs) -> LanguageModel:
    """Factory to create a language model instance."""
    if model_type == "together":
        return TogetherAILanguageModel(**kwargs)
    else:
        raise ValueError(f"Unsupported language model type: {model_type}")


# ----------------- SIMPLE TEST SECTION -----------------

if __name__ == "__main__":
    lm = get_language_model()

    prompt = "What is the capital of Peru?"
    response = lm.generate(prompt=prompt)

    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
