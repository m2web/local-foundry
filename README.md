# Local Foundry

A local RAG (Retrieval-Augmented Generation) application using Microsoft Foundry for running AI models locally.

## Features

- **RAG Implementation**: Uses LangChain with ChromaDB for semantic search and retrieval
- **Local LLM**: Runs Phi-4 mini model via Microsoft Foundry
- **Vector Embeddings**: HuggingFace BAAI/bge-small-en-v1.5 for CPU-optimized embeddings
- **Interactive CLI**: Query interface with streaming responses
- **Source Citations**: Displays markdown-formatted source references

## Demo Project: Rush Scholar

The included `rush_scholar.py` demonstrates RAG capabilities with a music-themed knowledge base. It answers questions by retrieving relevant context and generating informed responses.

### How It Works

1. **Ingestion**: Loads JSONL data and creates vector embeddings
2. **Retrieval**: Performs semantic search to find relevant content
3. **Generation**: Sends context to local LLM for answer generation
4. **Citations**: Displays source materials in markdown table format

## Prerequisites

- Python 3.11+
- Microsoft Foundry CLI installed and running
- Phi-4-mini-instruct model downloaded

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/m2web/local-foundry.git
   cd local-foundry
   ```

2. Install dependencies using `uv`:

   ```bash
   uv sync
   ```

3. Start Microsoft Foundry service:

   ```bash
   foundry service start
   ```

4. Verify the model is available:

   ```bash
   foundry model list
   ```

## Usage

Run the Rush Scholar demo:

```bash
uv run rush_scholar.py
```

Example queries:
- "What themes appear in the Hemispheres album?"
- "What was the conflict of the brain's hemispheres?"
- "Describe the symbolism in The Trees"

Type `exit` to quit.

## Configuration

Update these variables in `rush_scholar.py` to match your setup:

```python
FOUNDRY_BASE_URL = "http://127.0.0.1:53356/v1/chat/completions"
MODEL_NAME = "Phi-4-mini-instruct-generic-cpu:5"
DATA_FILE = "rush_lyrics_for_indexing.jsonl"
```

Check your Foundry service port with:

```bash
foundry service status
```

## Project Structure

```text
local-foundry/
├── rush_scholar.py          # Main RAG application
├── rush_lyrics_for_indexing.jsonl  # Sample data
├── rush_index/              # ChromaDB vector store (auto-generated)
├── rush_scholar_demo.md     # Presentation output example
├── pyproject.toml           # Project dependencies
└── README.md                # This file
```

## Dependencies

- **langchain**: LLM application framework
- **chromadb**: Vector database for embeddings
- **sentence-transformers**: Embedding models
- **requests**: HTTP client for Foundry API

See [pyproject.toml](pyproject.toml) for complete dependency list.

## License

MIT
