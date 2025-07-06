# 🤖 RAG PDFBot - Server

This is the FastAPI backend for the RAG PDFBot. It handles PDF processing, vectorstore embedding, LLM chain execution, and API endpoints.

---

## Features

- ✅ Upload and process PDFs
- 🧠 Chat with LLM using vectorstore retrieval
- 🔍 Inspect document chunks via similarity search
- 🌐 Supports multiple providers (Groq, Gemini)

---

## Project Structure

```
server/
├── api/                        # FastAPI routes and schemas
├── config/                     # Environment and constants
├── core/                       # LLM logic, vectorstore, processing
├── utils/                      # Logger and helpers
├── main.py                     # App entry point
```

---

## 📦 Installation

1. **Clone the repo**

```bash
git clone https://github.com/Zlash65/rag-bot-fastapi.git
cd rag-bot-fastapi
```

2. **Create a virtual environment (optional)**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
cd server

pip3 install -r requirements.txt
```

---

## Configuration

Set your API keys in `config/settings.py`:

- **Groq**: [console.groq.com](https://console.groq.com/)
- **Gemini**: [ai.google.dev](https://ai.google.dev)

```python
GROQ_API_KEY = "your_groq_key"
GOOGLE_API_KEY = "your_google_key"
```

---

## ▶️ Usage

Run the app:

```bash
cd rag-bot-fastapi/server

uvicorn main:app --reload
```

---

## API Endpoints

- `/upload_and_process_pdfs`
- `/chat`
- `/vector_store/count/{provider}`
- `/vector_store/search`
- `/llm`
- `/llm/{provider}`
- `/health`

## Logging

Logs are printed to the console and controlled via `utils/logger.py`.
