import google.genai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_embedding(text):
    response = client.models.embed_content(
        model='text-embedding-004',
        content=text
    )
    return response.embeddings[0].values

def load_documents():
    with open('docs.json', 'r') as f:
        docs = json.load(f)
    return docs

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size // 10):   
        chunk = ' '.join(words[i:i + chunk_size // 10])
        if chunk:
            chunks.append(chunk)
    return chunks

def generate_embeddings():
    docs = load_documents()
    vector_store = []
    for doc in docs:
        chunks = chunk_text(doc['content'])
        for chunk in chunks:
            embedding = get_embedding(chunk)
            vector_store.append({
                'title': doc['title'],
                'chunk': chunk,
                'embedding': embedding
            })
    return vector_store

if __name__ == "__main__":
    vectors = generate_embeddings()
    with open('vector_store.json', 'w') as f:
        json.dump(vectors, f)