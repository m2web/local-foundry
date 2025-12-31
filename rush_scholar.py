import json
import os
import sys
import requests
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Ensure port matches your 'foundry service status'
FOUNDRY_BASE_URL = "http://127.0.0.1:53356/v1/chat/completions"
# Must match the EXACT ID from 'foundry model list'
MODEL_NAME = "Phi-4-mini-instruct-generic-cpu:5" 
DATA_FILE = "rush_lyrics_for_indexing.jsonl"
DB_DIR = "./rush_index"

class RushScholar:
    def __init__(self):
        print("--- Initializing Rush Scholar ---")
        # Embedding model for CPU (BAAI is high performance/low memory)
        self.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        self.vector_db = None

    def ingest_data(self):
        """Loads JSONL, chunks text, and creates/loads the Vector DB."""
        if os.path.exists(DB_DIR):
            print(f"Loading existing index from {DB_DIR}...")
            self.vector_db = Chroma(persist_directory=DB_DIR, embedding_function=self.embeddings)
        else:
            print(f"Creating new index from {DATA_FILE}...")
            docs = []
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    docs.append(Document(
                        page_content=data["content"],
                        metadata={
                            "title": data["metadata"]["title"], 
                            "album": data["metadata"]["album"]
                        }
                    ))
            
            # Split by double-newlines to keep verses intact
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800, 
                chunk_overlap=100,
                separators=["\n\n", "\n", " "]
            )
            split_docs = splitter.split_documents(docs)
            
            self.vector_db = Chroma.from_documents(
                documents=split_docs, 
                embedding=self.embeddings,
                persist_directory=DB_DIR
            )
            print(f"Successfully indexed {len(split_docs)} segments.")

    def ask(self, query):
        # 1. RETRIEVAL
        # We increase k to 4 to get a broader range of sources
        results = self.vector_db.similarity_search(query, k=10)
        
        if not results:
            print("No matching lyrics found in the index.")
            return

        # 2. SOURCE EXTRACTION
        # We use .get() to avoid crashes if 'album' is missing from the index
        context_parts = []
        source_list = []
        
        for d in results:
            title = d.metadata.get('title', 'Unknown Song')
            album = d.metadata.get('album', 'Unknown Album')
            context_parts.append(f"Song: {title} (Album: {album})\n{d.page_content}")
            source_list.append(f"| {album} | {title} |")

        # Unique, sorted list of sources
        unique_sources = sorted(list(set(source_list)))
        context_text = "\n\n".join(context_parts)

        # 3. LLM PAYLOAD
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are a Rush Scholar. Answer using the context. Cite albums."},
                {"role": "user", "content": f"CONTEXT:\n{context_text}\n\nQUESTION: {query}"}
            ],
            "stream": True,
            "max_tokens": 1024
        }

        # 4. EXECUTION
        print(f"\n--- Rush Scholar Analysis ---")
        try:
            response = requests.post(FOUNDRY_BASE_URL, json=payload, stream=True, timeout=60)
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8').replace('data: ', '')
                    if decoded.strip() == '[DONE]': break
                    try:
                        chunk = json.loads(decoded)
                        print(chunk['choices'][0]['delta'].get('content', ''), end="", flush=True)
                    except: continue
            
            # THE CITATION BOX
            print("\n\n" + "═"*30)
            print("📜 SOURCES CONSULTED:")
            print("| Album | Song |")
            print("|-------|------|")
            if not unique_sources or "Unknown Album" in unique_sources[0]:
                print("⚠️  Warning: Metadata not found in current index.")
                print("Try deleting the 'rush_index' folder and restarting the script.")
            else:
                for s in unique_sources:
                    print(f"{s}")
            print("═"*30)

        except Exception as e:
            print(f"\nError: {e}")

# ==========================================
# 3. EXECUTION
# ==========================================
if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found in current directory.")
        sys.exit(1)

    scholar = RushScholar()
    scholar.ingest_data()
    
    print("\nRush Scholar is online. Ask about themes, lyrics, or albums.")
    print("(Type 'exit' to quit)\n")
    
    while True:
        user_input = input("Query > ")
        if user_input.lower() in ['exit', 'quit']:
            break
        if user_input.strip():
            scholar.ask(user_input)