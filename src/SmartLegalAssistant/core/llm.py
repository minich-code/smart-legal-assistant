"""
Language model integration for response generation.
"""
import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class LanguageModel(ABC):
    """Base class for language models."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the language model."""
        pass

class TogetherAILanguageModel(LanguageModel):
    """Implementation using Together AI."""
    
    def __init__(self, model_name: str = "mistralai/Mistral-Small-24B-Instruct-2501", api_key: str = None):
        """Initialize Together AI language model.
        
        Args:
            model_name: The model to use
            api_key: The Together AI API key (defaults to env var)
        """
        from together import Together
        
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("TOGETHER_API_KEY")
        
        if not self.api_key:
            raise ValueError("Together AI API key not found")
        
        self.client = Together(api_key=self.api_key)
    
    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1000, 
                 stop_sequences: Optional[List[str]] = None) -> str:
        """Generate a response using Together AI.
        
        Args:
            prompt: The input prompt
            temperature: Controls randomness (lower = more deterministic)
            max_tokens: Maximum tokens to generate
            stop_sequences: Optional list of strings to stop generation
            
        Returns:
            Generated text response
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop_sequences
        )
        
        return response.choices[0].message.content

# Factory function to get the right language model
def get_language_model(model_type: str = "together", **kwargs) -> LanguageModel:
    """Factory function to create language models.
    
    Args:
        model_type: Type of model to use ('together', etc.)
        **kwargs: Additional configuration for the model
        
    Returns:
        A language model instance
    """
    if model_type == "together":
        return TogetherAILanguageModel(**kwargs)
    else:
        raise ValueError(f"Unsupported language model type: {model_type}")