from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="langgraph_local",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.9",
    description="A modular language processing system with LLM-agnostic architecture",
    author="Your Name", 
    license="Apache 2.0",
)
