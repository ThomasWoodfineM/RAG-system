# RAG System for Food Consumption Report

## Prerequisites

- Python 3.8+
- A Google API key for accessing Gemini models (https://aistudio.google.com/app/apikey)

## Setup

1. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a file named `gemini_api_key.txt` in the project root and paste your Google API key into it.

## Project Structure

- `data_processor.py`: Processes markdown files into structured data.
- `embedding_store.py`: Creates and manages the vector store using Chroma.
- `rag_system.py`: Implements the RAG system using LangChain and Google's Generative AI.
- `main.py`: The main script to run the entire system.
