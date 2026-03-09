# 🤖 GenAI Assistant with RAG

Welcome! This is a friendly, production-ready chat assistant that uses smart retrieval to answer your questions based on a knowledge base. No more guessing – it pulls real info from documents!

## 🌟 What Makes It Special?
- **Smart Answers**: Uses embeddings to find the most relevant info, then generates human-like responses.
- **No Hallucinations**: If it doesn't know, it honestly says so.
- **Conversational**: Remembers your chat history for natural conversations.
- **Easy to Use**: Simple web interface, no complex setup.
- **Free Tier**: Uses Google Gemini (free up to certain limits)!

## 🚀 Quick Start (Super Easy!)
1. **Get Your Google API Key**: Go to [aistudio.google.com](https://aistudio.google.com/) and create a free account. Generate an API key.
2. **Add the Key**: Open `Backend/.env` and paste your key: `GOOGLE_API_KEY=your_key_here`
3. **Install Stuff**: In the Backend folder, run `pip install -r requirements.txt`
4. **Prep the Knowledge**: Run `python embeddings.py` (this turns documents into searchable vectors).
5. **Launch the Brain**: Run `python App.py` – your server starts!
6. **Chat Away**: Open `Frontend/index.html` in your browser and start asking questions!

## 💬 Try These Questions
- "How do I reset my password?"
- "What's two-factor authentication?"
- "How can I contact support?"

The assistant will give helpful, grounded answers!

## 🏗 How It Works (Under the Hood)
1. **Documents** → Split into chunks → **Turn into Vectors** (embeddings)
2. **Your Question** → Find similar vectors → **Grab Top Matches**
3. **Matches + Your Question + Chat History** → **AI Generates Answer**

## 📁 Project Structure
- `Backend/`: Python code for the brain (API, RAG, embeddings)
- `Frontend/`: Simple HTML chat interface
- `docs.json`: Your knowledge base
- `vector_store.json`: Pre-computed embeddings

## 🛠 Tech Used
- Python (Flask for API)
- Google Gemini (for embeddings and chat)
- HTML/JS (for the chat UI)
- Scikit-learn (for similarity search)

Enjoy chatting with your new AI friend! If something's off, check the console or restart the server. 😊