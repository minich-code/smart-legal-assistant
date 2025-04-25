
"""
Language model integration for response generation 
"""

import os 
from typing import List, Dict, Any, Optional 
from abc import ABC, abstractmethod
from together import Together 

class LanguageModel(ABC):

    """Language model interface for response generation"""

    pass 


class TogetherAILanguageModel(LanguageModel):
    """Factory class for language models currently using Together AI"""

    def __init__(self, model_name: str = "mistralai/Mistral-Small-24B-Instruct-2501", api_key:str = None):
        """Initialize Together AI Language model model.

        Args:
            model_name (str, optional): The name of the embedding model".
            api_key (str, optional): The Together AI API key for Together AI. Defaults to None. (Default to env variable)

        """

        self.model_name = model_name
        self.api_key = api_key or os.getenv("TOGETHERAI_API_KEY")

        if not self.api_key:
            raise ValueError("Please provide a Together AI API key or set the TOGETHER AI_API_KEY environment variable.")
        
        self.client = Together(api_key = self.api_key)

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1000,
                 stop_sequences: Optional[List[str]] = None) -> str:
        
        """ Generate a response using the language model.

        Args:
            prompt (str): The prompt for the language model. (Input prompt)
            temperature (float): The temperature parameter for the language model. (Lower = more deterministic)
            max_tokens (int): The maximum number of tokens to generate.
            stop_sequences (Optional[List[str]]): A list of stop sequences for the language model.
            
            
        Returns:
            str: The generated response from the language model.
        """
        response = self.client.chat.Completion.create(
            model=self.model_name,
            messages = [{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop_sequences
        )
        return response.choices[0]["text"]
    

class OpenAILanguageModel(LanguageModel):
    """Factory class for language models currently using OpenAI"""

    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key:str = None):
        """Initialize OpenAI Language model model.

        Args:
            model_name (str, optional): The name of the embedding model.".
            api_key (str, optional): The OpenAI API key for OpenAI. Defaults to None. (Default to env variable)

        """

        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("Please provide a OpenAI API key or set the OPENAI API_KEY environment variable.")
        
        self.client = openai(api_key = self.api_key)


    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1000,
                 stop_sequences: Optional[List[str]] = None) -> str:
        
        """ Generate a response using the language model.

        Args:
            prompt (str): The prompt for the language model. (Input prompt)
            temperature (float): The temperature parameter for the language model. (Lower = more deterministic)
            max_tokens (int): The maximum number of tokens to generate.
            stop_sequences (Optional[List[str]]): A list of stop sequences for the language model.
            
            
        Returns:
            str: The generated response from the language model.
        """
        response = self.client.chat.Completion.create(
            model=self.model_name,
            messages = [{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop_sequences
        )
        return response['choices'][0]['message']['content']
    
        
        
        
