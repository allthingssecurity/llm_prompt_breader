"""
LLM interface for LLM-Picbreeder
"""
from typing import List, Dict, Any, Optional
from openai import OpenAI
from .config import settings
from .models import PromptGenome, PromptEvaluation

class LLMInterface:
    """Interface to interact with various LLM APIs"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.model = settings.DEFAULT_MODEL
    
    def generate_response(self, prompt: str, system_message: str = "") -> str:
        """Generate a response from the LLM"""
        if not self.client:
            # Return a mock response if no API key
            return f"Mock response to: {prompt[:50]}..."
        
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def evaluate_prompt_batch(self, prompts: List[PromptGenome]) -> List[PromptEvaluation]:
        """Generate responses for a batch of prompts"""
        evaluations = []
        
        for prompt in prompts:
            # For now, we'll use a simple system message
            # In practice, this might be part of the prompt genome
            system_message = "You are a helpful assistant."
            
            response = self.generate_response(prompt.content, system_message)
            
            evaluation = PromptEvaluation(
                prompt_id=prompt.id,
                output_content=response,
                rating=0.0  # Will be set by users
            )
            
            evaluations.append(evaluation)
        
        return evaluations