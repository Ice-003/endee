# Developer Copilot with Codebase Memory (RAG using Endee)

## Overview
This project is a lightweight AI Developer Copilot that allows users to query a codebase using natural language.

## Features
- Code ingestion and chunking
- Semantic search using embeddings
- Retrieval-Augmented Generation (RAG)
- Vector storage (Endee-based concept)

## How Endee is Used
Endee acts as the vector database to store embeddings of code chunks and retrieve relevant context using similarity search.

## Workflow
1. Load code files
2. Convert into embeddings
3. Store in vector database
4. Retrieve relevant chunks
5. Generate response

## Setup
```bash
pip install sentence-transformers numpy
python app.py