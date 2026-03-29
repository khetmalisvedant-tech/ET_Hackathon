<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/23b56905-a1ee-44bd-9728-76964f77e75e" /># 🚀 AutoFlow AI — Multi-Agent Autonomous Workflow System

## 🌐 Live Demo

👉 Frontend: https://et-hackathon-nu.vercel.app
👉 Backend API: https://et-hackathon-o4iv.onrender.com

## 🎯 Problem Statement

This project is built for **ET AI Hackathon 2026** under:

### 🟢 Agentic AI for Autonomous Enterprise Workflows

AND

### 🟢 Domain-Specialized AI Agents (Agriculture)

---

## 🧠 What is AutoFlow AI?

AutoFlow AI is a **multi-agent intelligent system** that autonomously processes user queries and executes a complete workflow:

1. 🌱 Decision Making
2. ⚡ Action Planning
3. 📊 Monitoring
4. ✅ Verification

All without human intervention.

---

## 🏗️ System Architecture

```
User Input
    ↓
Decision Agent (LLM-based reasoning)
    ↓
Action Agent (task execution plan)
    ↓
Monitoring Agent (environment tracking)
    ↓
Verification Agent (output validation)
    ↓
Final Response to User
```

---

## ⚙️ Tech Stack

### 🖥️ Frontend

* React (Vite)
* Tailwind CSS
* Deployed on Vercel

### 🔧 Backend

* FastAPI
* Python
* Multi-agent architecture

### 🧠 AI Layer

* Groq API (LLaMA 3 model)

### 🌍 Data Integration

* Weather API (real-time / fallback)
* Geolocation API

---

## 🔥 Key Features

* ✅ Multi-agent autonomous workflow
* ✅ Real-time weather-based decision making
* ✅ Water Stress Index (WSI) calculation
* ✅ Intelligent farming recommendations
* ✅ Error-resilient fallback system
* ✅ Agent execution logs (visible in UI)

---

## 📊 Workflow Example

### Input:

```
Should I irrigate my farm today?
```

### Output:

* 🌱 Decision → Irrigation recommended
* ⚡ Action → Start irrigation for 20 minutes
* 📊 Monitoring → Track humidity & temperature
* ✅ Verification → Action validated

---

## 🧪 How It Works

1. User enters a query
2. System fetches location + weather
3. Calculates WSI (Water Stress Index)
4. Agents collaborate to produce output
5. Response is returned in structured format

---

## ⚠️ Error Handling (Important)

To ensure system stability:

* Fallback logic is implemented if AI fails
* Each agent is isolated using try/catch
* Workflow continues even if one component fails

This ensures **consistent demo performance**

---

## 🛠️ Local Setup

### 1. Clone Repo

```bash
git clone https://github.com/khetmalisvedant-tech/ET_Hackathon.git
cd ET_Hackathon
```

---

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Run backend:

```bash
uvicorn main:app --reload
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🚀 Deployment

### Backend (Render)

* Root Directory: `backend`
* Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

---

### Frontend (Vercel)

Environment Variable:

```env
VITE_API_URL=https://et-hackathon-o4iv.onrender.com
```

---

## 📹 Demo Video


👉 (Add your video link here — Google Drive / YouTube)

---

## 📐 Architecture Diagram
<img width="1536" height="1024" alt="architecture png" src="https://github.com/user-attachments/assets/820f0e9f-e8f2-4c68-b2a6-b7c866a276a2" />


---

## 📈 Impact Model

### Problem:

Farmers rely on manual decisions → inefficient & inconsistent

### Solution:

AutoFlow AI automates:

* Decision-making
* Action planning
* Monitoring

### Impact:

* ⏱️ Saves decision time
* 📊 Improves accuracy using data
* 🤖 Enables autonomous workflows

---

## 🏆 Why This Project Stands Out

* Full **multi-agent system** (not single LLM call)
* Handles **real-world uncertainty** (fallback logic)
* Demonstrates **autonomous execution**
* Built for **scalability and real-world use**

---

## 👨‍💻 Author

Vedant
GitHub: https://github.com/khetmalisvedant-tech

---

## 🙌 Acknowledgements

* ET AI Hackathon 2026
* Groq (LLM API)
* Open-source community

## ⭐ Final Note

This project demonstrates how **AI agents can collaborate to solve real-world problems autonomously**, making workflows faster, smarter, and more reliable.

```
"From input → decision → action → validation — fully automated."
```
