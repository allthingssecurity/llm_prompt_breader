"""
Evolution engine for LLM-Picbreeder
"""
import random
import string
from typing import List, Dict, Any
from .models import PromptGenome, PromptEvaluation
from .config import settings

class PromptEvolver:
    """Handles the evolutionary operations for prompts"""
    
    def __init__(self):
        self.mutation_rate = settings.MUTATION_RATE
        self.crossover_rate = settings.CROSSOVER_RATE
        self.population_size = settings.POPULATION_SIZE
    
    def initialize_population(self, base_prompt: str = "", size: int = None) -> List[PromptGenome]:
        """Create an initial population of prompt variants"""
        if size is None:
            size = self.population_size
            
        population = []
        for i in range(size):
            # Create variations of the base prompt
            variant = self._mutate_prompt(base_prompt, initial=True)
            genome = PromptGenome(
                content=variant,
                metadata={"source": "initial_population", "variant_id": i}
            )
            population.append(genome)
            
        return population
    
    def _mutate_prompt(self, prompt: str, initial: bool = False) -> str:
        """Apply mutations to a prompt"""
        if initial:
            # For initial population, apply more substantial variations
            mutations = [
                self._add_instruction,
                self._change_tone,
                self._add_example,
                self._reorder_elements
            ]
            mutation = random.choice(mutations)
            return mutation(prompt)
        
        # For evolutionary mutations
        if random.random() < self.mutation_rate:
            mutations = [
                self._add_instruction,
                self._change_tone,
                self._substitute_words,
                self._add_constraints,
                self._remove_elements
            ]
            
            # Apply one or more mutations
            num_mutations = random.randint(1, 2)
            for _ in range(num_mutations):
                if prompt:  # Only mutate non-empty prompts
                    mutation = random.choice(mutations)
                    prompt = mutation(prompt)
                    
        return prompt
    
    def _add_instruction(self, prompt: str) -> str:
        """Add an instruction to the prompt"""
        instructions = [
            "Please be very detailed in your response.",
            "Respond in a professional tone.",
            "Explain your reasoning step by step.",
            "Be concise and to the point.",
            "Use examples to illustrate your points."
        ]
        
        instruction = random.choice(instructions)
        if prompt:
            return f"{prompt}\n\n{instruction}"
        return instruction
    
    def _change_tone(self, prompt: str) -> str:
        """Change the tone of the prompt"""
        tone_changes = [
            "You are a helpful assistant.",
            "You are an expert in the field.",
            "You are explaining to a beginner.",
            "You are a creative writer.",
            "You are a critical analyst."
        ]
        
        # Replace or add tone instruction
        tone = random.choice(tone_changes)
        if "You are" in prompt:
            lines = prompt.split('\n')
            for i, line in enumerate(lines):
                if "You are" in line:
                    lines[i] = tone
                    return '\n'.join(lines)
            return f"{tone}\n\n{prompt}"
        else:
            return f"{tone}\n\n{prompt}"
    
    def _substitute_words(self, prompt: str) -> str:
        """Substitute words with synonyms"""
        # Simple word substitution - in practice, you might use a thesaurus API
        substitutions = {
            "good": ["excellent", "outstanding", "superior", "exceptional"],
            "bad": ["poor", "substandard", "inferior", "unsatisfactory"],
            "important": ["crucial", "vital", "essential", "significant"],
            "explain": ["describe", "elaborate", "clarify", "detail"],
            "simple": ["basic", "straightforward", "elementary", "clear"]
        }
        
        words = prompt.split()
        for i, word in enumerate(words):
            clean_word = word.lower().strip(string.punctuation)
            if clean_word in substitutions:
                words[i] = random.choice(substitutions[clean_word])
                
        return ' '.join(words)
    
    def _add_constraints(self, prompt: str) -> str:
        """Add constraints to the prompt"""
        constraints = [
            "Limit your response to 100 words.",
            "Include at least 3 examples.",
            "Structure your response as a list.",
            "Use technical terminology.",
            "Avoid jargon and acronyms."
        ]
        
        constraint = random.choice(constraints)
        return f"{prompt}\n\n{constraint}"
    
    def _remove_elements(self, prompt: str) -> str:
        """Remove parts of the prompt"""
        lines = prompt.split('\n')
        if len(lines) > 1:
            # Remove a random line (but not the first one)
            idx = random.randint(1, len(lines) - 1)
            lines.pop(idx)
            return '\n'.join(lines)
        return prompt
    
    def _add_example(self, prompt: str) -> str:
        """Add an example to the prompt"""
        examples = [
            "For example: If asked about photosynthesis, you might explain...",
            "Example format: Start with a definition, then provide applications.",
            "As an illustration: When discussing gravity, consider..."
        ]
        
        example = random.choice(examples)
        return f"{prompt}\n\n{example}"
    
    def _reorder_elements(self, prompt: str) -> str:
        """Reorder elements in the prompt"""
        lines = prompt.split('\n')
        if len(lines) > 2:
            # Shuffle middle lines
            middle = lines[1:-1]
            random.shuffle(middle)
            lines = [lines[0]] + middle + [lines[-1]]
            return '\n'.join(lines)
        return prompt
    
    def crossover(self, parent1: PromptGenome, parent2: PromptGenome) -> PromptGenome:
        """Create a new prompt by combining two parents"""
        if random.random() > self.crossover_rate:
            # Return one of the parents without crossover
            return random.choice([parent1, parent2])
        
        # Simple crossover - combine parts of both prompts
        lines1 = parent1.content.split('\n')
        lines2 = parent2.content.split('\n')
        
        # Create child by combining lines from both parents
        child_lines = []
        max_lines = max(len(lines1), len(lines2))
        
        for i in range(max_lines):
            if i < len(lines1) and i < len(lines2):
                # Choose line from either parent
                child_lines.append(random.choice([lines1[i], lines2[i]]))
            elif i < len(lines1):
                child_lines.append(lines1[i])
            else:
                child_lines.append(lines2[i])
        
        child_content = '\n'.join(child_lines)
        
        # Create new genome
        child = PromptGenome(
            content=child_content,
            metadata={
                "source": "crossover",
                "parent1_id": parent1.id,
                "parent2_id": parent2.id
            },
            parent_id=parent1.id  # Arbitrarily choose first parent as direct parent
        )
        
        return child
    
    def evolve_population(self, population: List[PromptGenome], 
                         evaluations: List[PromptEvaluation]) -> List[PromptGenome]:
        """Create a new generation from the current population"""
        # Sort population by evaluation ratings
        rated_prompts = []
        for prompt in population:
            # Find evaluations for this prompt
            prompt_evals = [e for e in evaluations if e.prompt_id == prompt.id]
            if prompt_evals:
                avg_rating = sum(e.rating for e in prompt_evals) / len(prompt_evals)
                rated_prompts.append((prompt, avg_rating))
            else:
                rated_prompts.append((prompt, 0.0))
        
        # Sort by rating (descending)
        rated_prompts.sort(key=lambda x: x[1], reverse=True)
        
        # Select top performers (tournament selection)
        selected = [prompt for prompt, rating in rated_prompts[:self.population_size//2]]
        
        # Create new population through crossover and mutation
        new_population = []
        
        # Keep some of the best unchanged (elitism)
        elite_count = max(1, self.population_size // 5)
        new_population.extend(selected[:elite_count])
        
        # Fill the rest with offspring
        while len(new_population) < self.population_size:
            # Select parents
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            
            # Create child
            if parent1.id != parent2.id:  # Ensure different parents
                child = self.crossover(parent1, parent2)
            else:
                # If same parent, just mutate
                child = PromptGenome(
                    content=parent1.content,
                    metadata={"source": "mutation", "parent_id": parent1.id}
                )
            
            # Apply mutation
            child.content = self._mutate_prompt(child.content)
            new_population.append(child)
        
        return new_population