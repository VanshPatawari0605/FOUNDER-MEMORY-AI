# 🚀 Founder Memory AI

An AI-powered second brain for founders that remembers meetings, documents, decisions, customer conversations, and company knowledge, enabling natural language search and intelligent question answering.

## ✨ Features

- 🔐 Secure JWT Authentication
- 🏢 Multi-Tenant Architecture
- 📄 PDF & DOCX Document Upload
- 🧠 AI-Powered Knowledge Retrieval
- 🔍 Semantic Search using Vector Embeddings
- 🤖 LangGraph Agent Workflow
- 💬 Conversational AI Chat
- 📌 Automatic Entity Extraction
- ⚡ Asynchronous Processing with Celery
- 📊 PostgreSQL + pgvector Vector Database

---

## 🛠 Tech Stack

### Frontend
- React
- Vite
- React Router
- Axios
- Context API

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- Celery
- Redis
- JWT Authentication

### AI Stack
- LangChain
- LangGraph
- Groq LLM
- Sentence Transformers
- HuggingFace Transformers

---

## 📂 Project Structure

```
Founder-Memory-AI
│
├── backend
│   ├── app
│   │   ├── agent
│   │   ├── api
│   │   ├── core
│   │   ├── models
│   │   ├── schemas
│   │   └── services
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 🧠 System Architecture

```
React Frontend
        │
        ▼
FastAPI Backend
        │
 ┌───────────────┐
 │ Authentication│
 │ Upload API    │
 │ Chat API      │
 │ Onboarding    │
 └───────────────┘
        │
        ▼
Celery + Redis
        │
        ▼
Embedding Generation
        │
        ▼
PostgreSQL + pgvector
        │
        ▼
LangGraph Agent
        │
        ▼
Groq LLM
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/VanshPatawari0605/FOUNDER-MEMORY-AI.git
cd FOUNDER-MEMORY-AI
```

---

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

docker compose up --build
```

Backend runs on:

```
http://localhost:8000
```

API Documentation:

```
http://localhost:8000/docs
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## 🔑 Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=

REDIS_URL=

GROQ_API_KEY=

EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## 🔄 Workflow

1. Register/Login
2. Complete AI Onboarding
3. Upload Documents
4. Documents are processed asynchronously
5. Text is chunked
6. Vector embeddings are generated
7. Stored inside PostgreSQL (pgvector)
8. Entities are extracted
9. Ask questions through AI Chat
10. LangGraph retrieves relevant context and generates responses

---

## 📸 Features

- Secure Authentication
- Founder Onboarding
- AI Chat Interface
- Document Upload
- Entity Explorer
- Semantic Search
- Context-Aware Responses
- Background Processing
- Multi-Tenant Data Isolation

---

## 📈 Future Improvements

- Meeting Transcript Integration
- Email Synchronization
- Slack Integration
- Google Drive Integration
- Voice Notes Support
- Company Timeline Visualization
- Role-Based Access Control
- Advanced Analytics Dashboard

---

## 👨‍💻 Author

**Vansh Patawari**

- GitHub: https://github.com/VanshPatawari0605
- LinkedIn: *(Add your LinkedIn profile here)*

---

## 📜 License

This project is licensed under the MIT License.
