# LLM-Picbreeder: Collaborative Prompt Evolution

## Interactive Tutorial

This is an interactive tutorial demonstrating the LLM-Picbreeder concept - applying collaborative evolutionary algorithms from Picbreeder to evolve prompts for Large Language Models.

[View the Interactive Tutorial](https://allthingssecurity.github.io/llm_prompt_breader/)

## Concept Overview

LLM-Picbreeder adapts the collaborative evolutionary approach from Picbreeder (which evolved images) to evolve prompts for LLMs like GPT-4. Instead of users selecting better images over generations, users select better prompts that produce more useful outputs from LLMs.

## How It Works

1. **Population Generation**: Start with a simple prompt and create variations
2. **Story Generation**: LLM generates stories for each prompt
3. **Community Rating**: Users rate the generated stories
4. **Evolution**: Top-rated prompts "breed" to create the next generation
5. **Branching**: Users can branch from successful prompts to explore new directions

## Key Benefits

- **Community Collaboration**: Leverage collective intelligence rather than individual efforts
- **Overcomes User Fatigue**: No single user needs to iterate endlessly
- **Preserves Innovations**: Good prompt variants are saved and built upon
- **Systematic Exploration**: Structured approach to exploring vast prompt design spaces

## Technical Implementation

The full LLM-Picbreeder project includes:

- Evolution engine for prompts with mutation and crossover operators
- Interface to LLM APIs
- Database for storing prompt lineages
- Web interface for user interaction
- Community rating system

[View the full project on GitHub](https://github.com/allthingssecurity/llm_prompt_breader)