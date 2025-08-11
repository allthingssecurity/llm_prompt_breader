"""
Main application for LLM-Picbreeder
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from . import models, evolver, llm_interface, database
from .config import settings

# Initialize the app
app = FastAPI(title="LLM-Picbreeder", description="Collaborative Evolution of LLM Prompts")

# Initialize components
evolver_instance = evolver.PromptEvolver()
llm_interface_instance = llm_interface.LLMInterface()

# Initialize database
database.init_db()

@app.get("/")
def read_root():
    return {
        "message": "LLM-Picbreeder API", 
        "description": "Collaborative Evolution of LLM Prompts and Outputs",
        "version": "0.1.0"
    }

@app.get("/prompts/", response_model=List[models.PromptGenome])
def get_prompts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Get a list of prompts"""
    db_prompts = db.query(database.DBPrompt).offset(skip).limit(limit).all()
    return [models.PromptGenome(
        id=p.id,
        content=p.content,
        template_vars=p.template_vars or {},
        metadata=p.metadata_json or {},
        creator_id=p.creator_id,
        parent_id=p.parent_id,
        created_at=p.created_at,
        complexity_score=p.complexity_score
    ) for p in db_prompts]

@app.post("/prompts/", response_model=models.PromptGenome)
def create_prompt(prompt: models.PromptGenome, db: Session = Depends(database.get_db)):
    """Create a new prompt"""
    db_prompt = database.DBPrompt(
        content=prompt.content,
        template_vars=prompt.template_vars,
        metadata_json=prompt.metadata,
        creator_id=prompt.creator_id,
        parent_id=prompt.parent_id,
        complexity_score=prompt.complexity_score
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    
    return models.PromptGenome(
        id=db_prompt.id,
        content=db_prompt.content,
        template_vars=db_prompt.template_vars or {},
        metadata=db_prompt.metadata_json or {},
        creator_id=db_prompt.creator_id,
        parent_id=db_prompt.parent_id,
        created_at=db_prompt.created_at,
        complexity_score=db_prompt.complexity_score
    )

@app.post("/evolve/")
def evolve_prompts(base_prompt: str, generations: int = 5):
    """Run an evolution experiment"""
    # This is a simplified version - in practice, you'd want to store results in the database
    
    # Initialize population
    population = evolver_instance.initialize_population(base_prompt)
    
    results = []
    
    for gen in range(generations):
        # Generate responses for each prompt
        evaluations = llm_interface_instance.evaluate_prompt_batch(population)
        
        # For this demo, we'll assign random ratings
        import random
        for eval in evaluations:
            eval.rating = random.uniform(1.0, 5.0)
        
        # Store generation results
        gen_results = {
            "generation": gen,
            "population": [p.dict() for p in population],
            "evaluations": [e.dict() for e in evaluations]
        }
        results.append(gen_results)
        
        # Evolve to next generation
        if gen < generations - 1:  # Don't evolve after the last generation
            population = evolver_instance.evolve_population(population, evaluations)
    
    return {"evolution_results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)