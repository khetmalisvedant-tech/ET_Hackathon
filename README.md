# 🚀 ET Hackathon Project – Multi-Agent AI System (AutoFlow AI)

## 🧠 Overview

AutoFlow AI is a **multi-agent collaboration system** designed to automate complex workflows using intelligent AI agents.
The system mimics real-world team collaboration by assigning tasks to specialized agents such as planning, data processing, decision-making, execution, and validation.

This project is built for the **ET AI Hackathon 2026** and focuses on creating a **scalable, autonomous, and production-ready AI system**.

---

## 🎯 Problem Statement

Modern workflows require coordination between multiple roles (planner, analyst, executor, reviewer).
Manual coordination leads to:

* ❌ Delays
* ❌ Errors
* ❌ Lack of accountability
* ❌ Inefficient execution

👉 Our solution: **Automate collaboration using AI agents**

---

## 💡 Solution

AutoFlow AI introduces a **multi-agent architecture** where each agent has a specific responsibility:

| Agent                | Role                                |
| -------------------- | ----------------------------------- |
| 🧩 Planner Agent     | Breaks user request into tasks      |
| 📊 Data Agent        | Fetches and processes required data |
| 🧠 Decision Agent    | Chooses best strategy               |
| ⚙️ Action Agent      | Executes the task                   |
| ✅ Verification Agent | Validates output                    |
| 📈 Monitoring Agent  | Tracks progress & errors            |

---

## ⚙️ Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS
* Modern UI with chat interface

### Backend

* FastAPI
* Python
* REST APIs

### AI / LLM

* Groq API / OpenAI (configurable)
* Streaming responses

### Other Tools

* Uvicorn (server)
* dotenv (environment variables)

---

## 🏗️ Project Structure

```
ET_Hack/
│
├── backend/
│   ├── main.py
│   ├── engine.py
│   ├── routes/
│   ├── agents/
│   └── models/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── styles/
│
├── .gitignore
└── README.md
```

---

## 🚀 Features

* 🤖 Multi-agent collaboration system
* ⚡ Real-time AI responses (streaming)
* 🎨 Modern chat UI
* 🔄 Dynamic model switching
* 🧠 Intelligent task breakdown
* 📊 Workflow tracking
* 🔐 Secure API handling

---

## 🧪 How It Works

1. User enters a query
2. Planner agent breaks it into steps
3. Data agent gathers required info
4. Decision agent selects best approach
5. Action agent executes
6. Verification agent checks output
7. Final result returned to user

---

## 🛠️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ET_Hackathon.git
cd ET_Hackathon
```

---

### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file:

```
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
```

Run server:

```bash
uvicorn main:app --reload
```

---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 API Endpoints

| Method | Endpoint  | Description         |
| ------ | --------- | ------------------- |
| POST   | `/chat`   | Send user query     |
| GET    | `/health` | Server health check |

---

## 🧩 Future Improvements

* 🌍 Multi-language support
* 📱 Mobile app
* 🔌 Plugin system for agents
* 🧠 Memory-based AI (context retention)
* 📊 Dashboard analytics

---

## 🏆 Hackathon Highlights

* Unique multi-agent architecture
* Real-world workflow automation
* Scalable and modular design
* Production-ready approach

---

## 🔐 Security

* API keys stored in `.env`
* No sensitive data exposed
* Secure backend communication

---

## 👨‍💻 Author

Vedant Khetmali
ET Hackathon 2026 Participant

---

## ⭐ Acknowledgements

* OpenAI / Groq APIs
* FastAPI
* React Community

---

## 📌 Note

This project is actively under development as part of the hackathon.
Further improvements and features will be added.

---

## 🚀 Demo (Optional)

*Add deployment link here (Render / Vercel)*

---

## ❤️ Support

If you like this project, consider giving it a ⭐ on GitHub!
