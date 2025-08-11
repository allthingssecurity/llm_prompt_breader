#!/bin/bash
# Script to run LLM-Picbreeder

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check which command to run
if [ "$1" = "api" ]; then
    echo "Starting API server..."
    uvicorn llm_picbreeder.main:app --reload
elif [ "$1" = "streamlit" ]; then
    echo "Starting Streamlit app..."
    streamlit run llm_picbreeder/streamlit_app.py
elif [ "$1" = "cli" ]; then
    echo "Running CLI demo..."
    python -m llm_picbreeder.cli --demo
elif [ "$1" = "example" ]; then
    echo "Running example..."
    python -m llm_picbreeder.example
elif [ "$1" = "comprehensive" ]; then
    echo "Running comprehensive example..."
    python -m llm_picbreeder.comprehensive_example
elif [ "$1" = "test" ]; then
    echo "Running tests..."
    python -m unittest llm_picbreeder/test_evolver.py
else
    echo "Usage: ./run.sh [api|streamlit|cli|example|comprehensive|test]"
    echo ""
    echo "Commands:"
    echo "  api           - Start the FastAPI server"
    echo "  streamlit     - Start the Streamlit demo app"
    echo "  cli           - Run the CLI demo"
    echo "  example       - Run the basic example"
    echo "  comprehensive - Run the comprehensive example"
    echo "  test          - Run tests"
fi