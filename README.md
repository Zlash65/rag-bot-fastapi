# 👽 RAG PDFBot - V3 (FastAPI + Streamlit)

This is the **production-ready refactor** of [rag-bot-chroma](https://github.com/Zlash65/rag-bot-chroma), introducing a real separation between frontend (UI) and backend (logic) using **Streamlit** and **FastAPI** respectively. This modular architecture helps in scaling, extending, and deploying the bot in real-world environments.

---

<details>
  <summary> 🔗 Helpful Links </summary>

- 🧑‍💻 [Version 1 - Basic RAG PDFBot (FAISS)](https://github.com/Zlash65/rag-bot-basic)
- ✍️ [V1 Blog Walkthrough](https://dev.to/zlash65/building-a-rag-powered-pdf-chatbot-with-langchain-streamlit-and-faiss-9i9)

- 🧑‍💻 [Version 2 - Modular Streamlit + Chroma](https://github.com/Zlash65/rag-bot-chroma)
- ✍️ [V2 Blog Walkthrough](https://dev.to/zlash65/refactoring-rag-pdfbot-modular-design-with-langchain-streamlit-and-chromadb-41fn)

- 🧑‍💻 [Version 3 - Streamlit + FastAPI](https://github.com/Zlash65/rag-bot-fastapi)
- ✍️ [V3 Blog Walkthrough](https://dev.to/zlash65/rag-pdfbot-v3-from-prototype-to-production-ready-ish-58h7)

</details>

---

## 🔄 What Changed from `rag-bot-chroma`

| Feature | Version 2 | Version 3 |
|--------|-------------|--------------|
| Codebase | One Streamlit app | Split into `client/` + `server/` |
| PDF Upload | In Streamlit | Async FastAPI API |
| Chat | In Streamlit | Calls `/chat` API |
| Vectorstore | In UI | Controlled by backend |
| Model Options | Static | Dynamically fetched |
| Inspector | In sidebar | Main panel toggle |
| Splitting | `RecursiveTextSplitter` | `TokenTextSplitter` |
| UX | Crude | Responsive, clear, downloadable |
| Extendability | Hard | Easy to plug new LLMs, tools |

---

## 🧪 How It Looks

### Demo
![demo-gif](/assets/rag-bot-fastapi.gif)

---

## 🏗️ Architecture

![architecture](/assets/rag-bot-fastapi-architecture.png)

---

## 🚀 Features

- 📁 Upload multiple PDFs and chat with them
- 🔌 Choose from Groq or Gemini as LLM providers
- 🔎 Query inspector for vectorstore transparency
- 🧠 RAG with LangChain + ChromaDB
- 📦 Streamlit frontend, FastAPI backend
- 🧪 Token-based chunking for LLM precision
- 💬 Downloadable chat history
- 🧰 Tools for reset, undo, clear
- 🌐 Fully API-driven interaction

---

<details>
  <summary>🛠️ Tech Stack</summary>

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLMs**: Groq & Gemini via LangChain
- **Vector DB**: ChromaDB
- **Embeddings**: HuggingFace & Google GenAI
- **Chunking**: TokenTextSplitter (was RecursiveCharacterTextSplitter)
- **Parsing**: PyPDF
- **Orchestration**: LangChain Retrieval Chain

</details>

---

## 📦 Installation

```bash
git clone https://github.com/Zlash65/rag-bot-fastapi.git
cd rag-bot-fastapi
```

Setup Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install frontend:

```bash
cd client
pip3 install -r requirements.txt
```

Install backend:

```bash
cd ../server
pip3 install -r requirements.txt
```

---

## 🔐 API Keys Required

- **Groq API key** from [console.groq.com](https://console.groq.com/)
- **Google Gemini API key** from [ai.google.dev](https://ai.google.dev/)

Create a `.env` file:

```env
GROQ_API_KEY=your-groq-key
GOOGLE_API_KEY=your-google-key
```

---

## ▶️ Run the Bot

Start FastAPI backend:

```bash
# Terminal 1
cd server
uvicorn main:app --reload
```

Start Streamlit frontend:

```bash
# Terminal 2
cd client
streamlit run app.py
```

---

<details>
  <summary>📁 Project Structure</summary>

```bash
rag-bot-v3/
├── client/                         # Streamlit Frontend
│   ├── app.py                      # Main Streamlit entrypoint
│   ├── components/                 # UI modules
│   │   ├── chat.py
│   │   ├── inspector.py
│   │   └── sidebar.py
│   ├── state/
│   │   └── session.py              # Session state manager
│   ├── utils/
│   │   ├── api.py                  # Talks to backend
│   │   ├── config.py               # API_URL and config values
│   │   └── helpers.py              # API wrappers for frontend
│   ├── requirements.txt
│   └── README.md

├── server/                         # FastAPI Backend
│   ├── api/
│   │   ├── routes.py               # API endpoints
│   │   └── schemas.py              # Pydantic schemas for I/O
│   ├── core/
│   │   ├── document_processor.py   # Handles PDF validation and chunking
│   │   ├── llm_chain_factory.py    # Builds LLM chains and prompts
│   │   └── vector_database.py      # Embeddings + ChromaDB ops
│   ├── config/
│   │   └── settings.py             # App config, model provider setup
│   ├── utils/
│   │   └── logger.py               # Logging setup
│   ├── main.py                     # FastAPI app entrypoint
│   ├── requirements.txt
│   └── README.md

├── README.md                       # Root README (overview + instructions)
├── .gitignore
```

</details>

---

<details>
  <summary> 👓 Different Views </summary>

| View | Description |
|------|-------------|
| 💬 Chat | Renders chat bubbles, input box, and chat history download |
| 🔬 Inspector | Renders inspector to test vectorstore responses |

![views](/assets/rag-bot-fastapi-clean-ui-ux.gif)

</details>

---

<details>
  <summary>🧼 Tools Panel</summary>

| Button | Function |
|----------|--------|
| 🔄 Reset | Clears session state and reruns app |
| 🧹 Clear Chat | Clears chat + PDF submission |
| ↩️ Undo | Removes last question/response |

</details>

---

<details>
  <summary>📦 Download Chat History</summary>

Chat history is saved in the session state and can be exported as a CSV with the following columns:

| Question | Answer | Model Provider | Model Name | PDF File | Timestamp |
|----------|--------|----------------|------------|---------------------|-----------|
| What is this PDF about? | This PDF explains... | Groq | llama3-70b-8192 | file1.pdf, file2.pdf | 2025-07-03 21:00:00 |

</details>

---

<details>
  <summary>🙏 Acknowledgements</summary>

- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [Groq](https://console.groq.com/)
- [Google Gemini](https://ai.google.dev/)
- [Chroma](https://docs.trychroma.com/)

</details>

---

## 🧠 New to this Project?

Start from the basics:
👉 [Version 1 - rag-bot-basic](https://github.com/Zlash65/rag-bot-basic)

Understand modular design:
👉 [Version 2 - rag-bot-chroma](https://github.com/Zlash65/rag-bot-chroma)

Then return here for real-world patterns.

---

Happy building! 🛠️
