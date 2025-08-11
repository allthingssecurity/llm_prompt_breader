"""
Tests for LLM-Picbreeder
"""
import sys
import os
import unittest

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from llm_picbreeder import evolver, models

class TestPromptEvolver(unittest.TestCase):
    def setUp(self):
        self.evolver = evolver.PromptEvolver()
    
    def test_initialize_population(self):
        """Test that population initialization works"""
        base_prompt = "Write a story"
        population = self.evolver.initialize_population(base_prompt, size=5)
        
        self.assertEqual(len(population), 5)
        for prompt in population:
            self.assertIsInstance(prompt, models.PromptGenome)
            self.assertIn("Write a story", prompt.content)
    
    def test_mutate_prompt(self):
        """Test that prompt mutation works"""
        original = "Write a story about a cat"
        mutated = self.evolver._mutate_prompt(original)
        
        # The mutated prompt should be different (with high probability)
        # but still contain some elements of the original
        self.assertIsInstance(mutated, str)
    
    def test_crossover(self):
        """Test that crossover works"""
        parent1 = models.PromptGenome(content="Write a story about a dog", id=1)
        parent2 = models.PromptGenome(content="Describe a journey through space", id=2)
        
        child = self.evolver.crossover(parent1, parent2)
        
        self.assertIsInstance(child, models.PromptGenome)
        self.assertIsNotNone(child.content)
    
    def test_evolve_population(self):
        """Test that population evolution works"""
        # Create a simple population
        population = [
            models.PromptGenome(id=1, content="Prompt 1"),
            models.PromptGenome(id=2, content="Prompt 2"),
            models.PromptGenome(id=3, content="Prompt 3")
        ]
        
        # Create evaluations with different ratings
        evaluations = [
            models.PromptEvaluation(prompt_id=1, output_content="Output 1", rating=5.0),
            models.PromptEvaluation(prompt_id=2, output_content="Output 2", rating=3.0),
            models.PromptEvaluation(prompt_id=3, output_content="Output 3", rating=1.0)
        ]
        
        # Evolve the population
        new_population = self.evolver.evolve_population(population, evaluations)
        
        self.assertEqual(len(new_population), self.evolver.population_size)

if __name__ == "__main__":
    unittest.main()