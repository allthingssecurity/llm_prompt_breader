from setuptools import setup, find_packages

setup(
    name="llm-picbreeder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "numpy>=1.21.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.11.0",
        "streamlit>=1.25.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "llm-picbreeder=llm_picbreeder.cli:main",
        ],
    },
    author="AI Researcher",
    author_email="ai.researcher@example.com",
    description="Collaborative Evolution of LLM Prompts and Outputs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/llm-picbreeder",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
)