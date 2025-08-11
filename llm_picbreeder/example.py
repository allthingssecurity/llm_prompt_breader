"""
Example script demonstrating LLM-Picbreeder concepts
"""
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from llm_picbreeder import evolver, llm_interface, models

def main():
    print("LLM-Picbreeder Concept Demonstration")
    print("=" * 50)
    
    # Create an evolver
    prompt_evolver = evolver.PromptEvolver()
    
    # Start with a base prompt
    base_prompt = "Write a short story about a character who discovers a hidden talent"
    print(f"Base prompt: {base_prompt}")
    
    # Initialize a population of prompt variants
    print("\n1. Initializing population...")
    population = prompt_evolver.initialize_population(base_prompt, size=5)
    
    for i, prompt in enumerate(population):
        print(f"  Variant {i+1}: {prompt.content}")
    
    # Show how mutation works
    print("\n2. Demonstrating mutation...")
    mutated = prompt_evolver._mutate_prompt(base_prompt)
    print(f"  Original: {base_prompt}")
    print(f"  Mutated:  {mutated}")
    
    # Show how crossover works
    print("\n3. Demonstrating crossover...")
    parent1 = models.PromptGenome(content="Write a story about a brave knight", id=1)
    parent2 = models.PromptGenome(content="Describe a magical forest adventure", id=2)
    
    child = prompt_evolver.crossover(parent1, parent2)
    print(f"  Parent 1: {parent1.content}")
    print(f"  Parent 2: {parent2.content}")
    print(f"  Child:    {child.content}")
    
    print("\nThis demonstrates the core evolutionary mechanisms that would be used")
    print("in a full LLM-Picbreeder implementation.")

if __name__ == "__main__":
    main()