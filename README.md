# Local Foundry

![Local Foundry Header Banner](images/local_foundry_header.png)

A local Retrieval-Augmented Generation (RAG) demo that runs entirely on a single Windows machine using **Microsoft Foundry Local** for inference. The repository features the **"Rush Scholar"** — a searchable knowledge base of Rush lyrics that uses a local LLM to answer thematic questions with citations.

---

## 🚀 Highlights

- **100% Local**: No cloud required — inference, embeddings, and vector store run locally.
- **RAG Pattern**: Complete pipeline: Ingest → Chunk → Embed → Index → Retrieve → Generate.
- **Practical Fixes**: Includes "protocol-light" request code to avoid `openai.BadRequestError: 400` common with local OpenAI-compatible endpoints.
- **Optimized for Speed**: Uses CPU-optimized models for embeddings and inference.

## ✨ Features

- **RAG Implementation**: Powered by LangChain and ChromaDB.
- **Local LLM**: Runs the **Phi-4 mini** model via Microsoft Foundry.
- **Semantic Search**: Uses **HuggingFace BAAI/bge-small-en-v1.5** for high-quality, local embeddings.
- **Streaming Response**: Interactive CLI with real-time streaming throughput.
- **Citations**: Automatically generates markdown-formatted source references for every answer.

---

## 🛠 Tech Stack

- **Inference Engine**: [Microsoft Foundry Local](images/local_foundry_header.png)
- **LLM**: Phi-4-mini (CPU-optimized)
- **Vector Database**: ChromaDB
- **Embeddings**: BAAI/bge-small-en-v1.5
- **Environment**: `uv` for lightning-fast Python dependency management

---

## 🏗 Architecture

1. **Ingestion**: `rush_lyrics_for_indexing.jsonl` is parsed into documents with metadata (album, title).
2. **Chunking**: `RecursiveCharacterTextSplitter` uses `\n\n`-aware splitting to keep verses and prologues coherent.
3. **Vectorization**: Chunks are embedded with a 384-d BGE model and stored in ChromaDB.
4. **Retrieval**: Semantic search identifies the most relevant lyric chunks for the user's query.
5. **Inference**: Retrieved context is combined with a prompt and sent to the local Phi-4-mini model for the final response.

---

## 💻 Get Started

### Prerequisites

- **Python 3.11+**
- [Microsoft Foundry CLI](images/local_foundry_header.png) installed and running.
- `Phi-4-mini-instruct` model downloaded in Foundry.

### Installation & Run

1. **Clone the repository**:

   ```bash
   git clone https://github.com/m2web/local-foundry.git
   cd local-foundry
   ```

2. **Sync Dependencies**:

   ```bash
   uv sync
   ```

3. **Start Microsoft Foundry**:

   ```bash
   foundry service start
   ```

4. **Verify Connectivity**:

   ```bash
   foundry model list
   foundry service status
   ```

5. **Run the Rush Scholar**:

   ```bash
   uv run rush_scholar.py
   ```

---

## 🎓 Demo: Rush Scholar

![Rush Scholar Hero Image](images/rush_scholar_hero.png)

The `rush_scholar.py` script demonstrates the full workflow. Try asking:

- *"What themes appear in the Hemispheres album?"*
- *"Compare the themes of Subdivisions and Middletown Dreams"*
- *"Describe the symbolism in The Trees"*

### Example Result

**Query**: *Compare the theme of 'Subdivisions' to 'Middletown Dreams'*

**Analysis**: Both songs examine suburban confinement and the desire to escape. 'Subdivisions' highlights social pressure to conform, while 'Middletown Dreams' focuses on the private inner life and longings of the dreamer.

**Sources Consulted**:

| Source | Track |
| --- | --- |
| Signals | Subdivisions |
| Power Windows | Middletown Dreams |

---

## 🛡 The "Error 400" Boss Fight

Local OpenAI-compatible endpoints often reject high-level client requests that include extra metadata or non-standard headers, resulting in `BadRequestError: 400`.

This project solves this with a **"protocol-light"** approach: minimal Python `requests` that send only the essential prompt and required fields. This ensures reliability across various local inference servers.

---

## 📂 Project Structure

- `rush_scholar.py`: Main RAG application and interactive CLI.
- `rush_lyrics_for_indexing.jsonl`: Sample dataset of Rush lyrics.
- `rush_index/`: Local ChromaDB vector store (generated on first run).
- `rush_scholar_demo.md`: Extended examples and documentation.
- `pyproject.toml`: Project metadata and dependencies managed by `uv`.

---

## 🔗 Resources & Contact

- **Full Write-up**: [My Local Rush Scholar](https://msquaredweb.gitlab.io/fyi/posts/my_local_rush_scholar/)
- **Author**: Mark McFadden
- **Website**: [markmcfadden.net](https://markmcfadden.net/)
- **Email**: <ai@markmcfadden.net>

---

Copyright © 2026 Mark McFadden. Licensed under the MIT License.
