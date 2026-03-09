from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from Rag import rag_pipeline

app = Flask(__name__)
CORS(app) 

sessions = {} 

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'sessionId' not in data or 'message' not in data:
        return jsonify({"error": "Invalid input. Provide sessionId and message."}), 400
    
    session_id = data['sessionId']
    message = data['message']
    
    if session_id not in sessions:
        sessions[session_id] = []
    
    history = sessions[session_id]
    
    try:
        reply, tokens_used, retrieved_chunks = rag_pipeline(message, history)

        history.append({'user': message, 'assistant': reply})
        return jsonify({
            "reply": reply,
            "tokensUsed": tokens_used,
            "retrievedChunks": retrieved_chunks
        })
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    
    if not os.path.exists('vector_store.json'):
        from embeddings import generate_embeddings
        vectors = generate_embeddings()
        with open('vector_store.json', 'w') as f:
            json.dump(vectors, f)
    app.run(debug=True, host='0.0.0.0', port=5000)