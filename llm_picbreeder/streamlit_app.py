"""
Streamlit app for LLM-Picbreeder
"""
import streamlit as st
import random
import time
from typing import List
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from llm_picbreeder import evolver, llm_interface, models

# Initialize session state
if 'population' not in st.session_state:
    st.session_state.population = []
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = []
if 'generation' not in st.session_state:
    st.session_state.generation = 0
if 'evolver' not in st.session_state:
    st.session_state.evolver = evolver.PromptEvolver()
if 'llm_interface' not in st.session_state:
    st.session_state.llm_interface = llm_interface.LLMInterface()

st.title("LLM-Picbreeder: Collaborative Prompt Evolution")
st.markdown("""
This demo applies the collaborative evolutionary concepts from the Picbreeder paper 
to LLM prompts. Instead of evolving images, we're evolving prompts that produce 
better outputs from language models.
""")

# Sidebar for controls
st.sidebar.header("Controls")

# Base prompt input
base_prompt = st.sidebar.text_area(
    "Base Prompt", 
    "Write a creative short story about a character who discovers they can communicate with animals",
    height=100
)

# Evolution parameters
generations = st.sidebar.slider("Generations", 1, 10, 3)
population_size = st.sidebar.slider("Population Size", 3, 15, 5)
mutation_rate = st.sidebar.slider("Mutation Rate", 0.0, 1.0, 0.1)
crossover_rate = st.sidebar.slider("Crossover Rate", 0.0, 1.0, 0.7)

# Update evolver parameters
st.session_state.evolver.mutation_rate = mutation_rate
st.session_state.evolver.crossover_rate = crossover_rate
st.session_state.evolver.population_size = population_size

# Initialize evolution
if st.sidebar.button("Initialize Evolution"):
    st.session_state.generation = 0
    st.session_state.population = st.session_state.evolver.initialize_population(base_prompt)
    st.session_state.evaluations = []
    st.sidebar.success("Evolution initialized!")

# Run generation
if st.sidebar.button("Run Next Generation") and st.session_state.population:
    with st.spinner("Generating responses..."):
        # Generate responses for current population
        st.session_state.evaluations = st.session_state.llm_interface.evaluate_prompt_batch(
            st.session_state.population
        )
        
        # For demo, assign random ratings
        for eval in st.session_state.evaluations:
            eval.rating = random.uniform(1.0, 5.0)
        
        st.session_state.generation += 1
        st.sidebar.success(f"Generation {st.session_state.generation} complete!")

# Evolve to next generation
if st.sidebar.button("Evolve Population") and st.session_state.evaluations:
    st.session_state.population = st.session_state.evolver.evolve_population(
        st.session_state.population, 
        st.session_state.evaluations
    )
    st.session_state.evaluations = []  # Clear evaluations for next generation
    st.sidebar.success("Population evolved!")

# Display current state
st.header(f"Current State: Generation {st.session_state.generation}")

if st.session_state.population:
    st.subheader("Current Population")
    
    # Display prompts and responses
    cols = st.columns(2)
    
    for i, prompt in enumerate(st.session_state.population):
        col = cols[i % 2]
        with col:
            st.markdown(f"**Prompt {i+1}**")
            st.text(prompt.content)
            
            # Find corresponding evaluation if it exists
            evaluation = None
            if st.session_state.evaluations:
                evaluation = st.session_state.evaluations[i] if i < len(st.session_state.evaluations) else None
            
            if evaluation:
                st.markdown("**Response:**")
                st.info(evaluation.output_content[:200] + "..." if len(evaluation.output_content) > 200 else evaluation.output_content)
                
                st.markdown("**Rating:**")
                st.progress(evaluation.rating / 5.0)
                st.write(f"{evaluation.rating:.2f}/5.0")
            
            st.markdown("---")
else:
    st.info("Initialize evolution to start")

# Explanation
st.header("How It Works")
st.markdown("""
1. **Initialization**: Start with a base prompt and create variations
2. **Evaluation**: Generate responses from an LLM for each prompt
3. **Selection**: Users rate the quality of responses (simulated here)
4. **Evolution**: Create new prompts by combining and mutating high-rated prompts
5. **Iteration**: Repeat the process to evolve better prompts over time

This approach allows collaborative discovery of effective prompts, similar to how Picbreeder enabled collaborative discovery of interesting images.
""")