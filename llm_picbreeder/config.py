"""
Configuration for LLM-Picbreeder
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite:///./llm_picbreeder.db"
    
    # Evolution parameters
    POPULATION_SIZE: int = 15
    MUTATION_RATE: float = 0.1
    CROSSOVER_RATE: float = 0.7
    
    # LLM settings
    DEFAULT_MODEL: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings()