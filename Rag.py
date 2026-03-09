import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def load_vector_store():
    with open('vector_store.json', 'r') as f:
        return json.load(f)

def get_query_embedding(query):
    response = client.models.embed_content(
        model='text-embedding-004',
        content=query
    )
    return response.embeddings[0].values

def retrieve_relevant_chunks(query, vector_store, top_k=3, threshold=0.7):
    query_emb = get_query_embedding(query)
    similarities = []
    for item in vector_store:
        sim = cosine_similarity([query_emb], [item['embedding']])[0][0]
        similarities.append((sim, item))
    similarities.sort(reverse=True, key=lambda x: x[0])
    top_chunks = [item for sim, item in similarities[:top_k] if sim >= threshold]
    return top_chunks

def generate_response(query, context, history):
    system_prompt = "You are a helpful assistant. Answer based on the provided context. If the context doesn't have the information, say so."
    
    conversation = system_prompt + "\n\n"
    for msg in history[-5:]:
        conversation += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n"
    
    context_text = "\n".join([chunk['chunk'] for chunk in context])
    prompt = f"Context:\n{context_text}\n\nQuestion: {query}"
    conversation += f"User: {prompt}\nAssistant:"
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=conversation
    )
    reply = response.text 
    tokens_used = len(reply.split()) + len(prompt.split())
    return reply, tokens_used

def rag_pipeline(query, history):
    vector_store = load_vector_store()
    relevant_chunks = retrieve_relevant_chunks(query, vector_store)
    if not relevant_chunks:
        return "I'm sorry, I don't have enough information to answer that question.", 0, 0
    reply, tokens = generate_response(query, relevant_chunks, history)
    return reply, tokens, len(relevant_chunks)