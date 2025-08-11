"""
Data models for LLM-Picbreeder
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class PromptGenome(BaseModel):
    """Represents a prompt as an evolvable genome"""
    id: Optional[int] = None
    content: str
    template_vars: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    creator_id: Optional[int] = None
    parent_id: Optional[int] = None
    created_at: datetime = None
    complexity_score: float = 0.0  # Based on length, structure, etc.
    
    model_config = {
        "from_attributes": True
    }

class PromptEvaluation(BaseModel):
    """Represents user evaluation of a prompt/output pair"""
    id: Optional[int] = None
    prompt_id: int
    output_content: str
    rating: float  # 1-5 scale
    user_id: Optional[int] = None
    created_at: datetime = None
    
    model_config = {
        "from_attributes": True
    }

class User(BaseModel):
    """Represents a user in the system"""
    id: Optional[int] = None
    username: str
    created_at: datetime = None
    
    model_config = {
        "from_attributes": True
    }

class EvolutionLineage(BaseModel):
    """Represents the evolutionary lineage of a prompt"""
    id: Optional[int] = None
    prompt_id: int
    ancestor_ids: List[int] = []
    generation: int = 0
    branch_point: Optional[int] = None
    
    model_config = {
        "from_attributes": True
    }