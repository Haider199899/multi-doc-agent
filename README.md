# Multi-Document Query Agent with LlamaIndex and OpenAI GPT-3.5 Turbo

This project demonstrates how to set up a basic multi-document query agent using [LlamaIndex](https://gpt-index.readthedocs.io/) and OpenAI's GPT-3.5 Turbo model. It allows querying across multiple documents by creating an index and retrieving relevant responses.

## Features

- Indexing multiple documents for easy querying
- Querying with OpenAI's GPT-3.5 Turbo model
- Simple and easy-to-use setup

## Prerequisites

- Python 3.7+
- An OpenAI API key for GPT-3.5 Turbo

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Haider199899/multi-doc-agent.git
   cd multi-doc-agent

2. **Setting virtual environment and installing dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. **Setting environment variables**:
   ```bash
   touch .env
   Add you API_KEY for accessing OpenAI model e.g : 
       OPENAI_API_KEY="XXXXXXX"
    
4. **Running the app**:
   ```bash
   python main.py
