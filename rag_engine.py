
import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer

class GmailRAG:
    def __init__(self, api_key):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        self.doc_strings = []
        self.index = None
        self.metadata = []

    def index_emails(self, documents):
        self.doc_strings = [d["page_content"] for d in documents]
        self.metadata = [d["metadata"] for d in documents]
        embeddings = self.embedder.encode(self.doc_strings)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))
        return len(documents)

    def query(self, question, k=3):
        q_embedding = self.embedder.encode([question])
        distances, indices = self.index.search(np.array(q_embedding), k)
        context = "\n---\n".join([self.doc_strings[i] for i in indices[0]])
        sources = [self.metadata[i] for i in indices[0]]
        
        prompt = f"""You are an AI email assistant. Answer based ONLY on the emails provided.

Context:
{context}

Question: {question}

Answer:"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 400
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            data = response.json()
            if "choices" in data:
                return {
                    "answer": data["choices"][0]["message"]["content"],
                    "sources": sources
                }
            else:
                error = data.get("error", {}).get("message", str(data))
                return {"answer": f"Groq error: {error}", "sources": sources}
        except Exception as e:
            return {"answer": f"Error: {str(e)}", "sources": sources}
