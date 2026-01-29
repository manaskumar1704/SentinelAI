# 🛡️ SentinelAI

SentinelAI is a state-of-the-art, AI-powered study-abroad counselling platform designed to guide students through the complexities of international education. By leveraging advanced LLMs (Google Gemini) and a deterministic 3-layer architecture, SentinelAI provides personalized recommendations, application guidance, and a persistent AI counsellor.

---

## 🚀 Key Features

- **🧠 Smart Onboarding**: Data-driven profiling to understand academic background, study goals, budget, and readiness. Supports both manual forms and conversational AI flows.
- **📊 Interactive Dashboard**: A central hub to track profile strength, current stages, and AI-generated to-do lists with real-time updates.
- **🤖 AI Counsellor (Core)**: A persistent AI agent powered by Google Gemini and a custom RAG pipeline that recommends universities, explains fit/risks, and performs actions on behalf of the user.
- **🎓 University Classification**: Intelligent grouping of universities into **Dream**, **Target**, and **Safe** categories based on user profile and acceptance probability.
- **🎓 University Locking**: A strategic flow where students lock-in target universities to unlock specific, tailored application guidance.
- **✅ Application Guidance**: Automated generation of timelines, document checklists, and task tracking for SOPs, transcripts, and exams.
- **✨ Premium UX**: Modern, responsive interface with glassmorphism aesthetics and smooth Framer Motion transitions.

---

## 🏗️ Project Structure

SentinelAI is organized as a monorepo with a 3-layer architecture for maximum reliability and scalability.

- **/frontend**: A polished Next.js 15 application built with TypeScript, Bun, and TailwindCSS. Uses Supabase for authentication and Framer Motion for premium animations.
- **/backend**: A high-performance FastAPI service handling AI orchestration, data management, and business logic. Uses `uv` for dependency management and SQLModel for database interactions.
- **/directives**: Contains Standard Operating Procedures (SOPs) in Markdown that define how the AI agent and backend modules operate.
- **AI Engine (within backend)**: A custom-built engine utilizing Google Gemini for fast inference and a RAG pipeline for context-aware counselling.

---

## 🛠️ Tech Stack

### Frontend

- **Framework**: Next.js 15 (App Router)
- **Runtime**: Bun
- **Authentication**: Supabase Auth
- **Animations**: Framer Motion
- **Styling**: TailwindCSS 4 + Vanilla CSS (Custom Design System)
- **State Management**: React Hooks & Context

### Backend

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **AI Engine**: Google Gemini (LLM Orchestration)
- **Database**: Supabase (PostgreSQL)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Dependency Management**: `uv`

---

## 🚦 Getting Started

### 1. Prerequisites

- **Bun** (for frontend)
- **Python 3.11+** and **uv** (for backend)
- **Supabase Account**: For Authentication and PostgreSQL database.
- **Google API Key**: For the AI Counsellor features (Gemini API).

### 2. Backend Setup

```bash
cd backend
uv sync
# Copy .env.example to .env and fill in your keys (Supabase, Google Gemini)
uv run uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
bun install
# Copy .env.example to .env.local and fill in your Supabase credentials
bun dev
```

---

## 📜 Architecture: The 3-Layer System

As outlined in `AGENTS.md`, this project follows a strict separation of concerns to bridge the gap between probabilistic AI and deterministic business logic:

1. **Layer 1: Directive (What to do)** - SOPs in `directives/` define the goals and rules.
2. **Layer 2: Orchestration (Decision making)** - The AI agent and routers handle routing and error management.
3. **Layer 3: Execution (Doing the work)** - Deterministic services in `backend/services/` handle the actual data processing and API calls.

---

## 🤝 Contributing

This project is built with a focus on modularity ("one feature, one file"). Please refer to `PLAN.md` for the core prototype flow and `AGENTS.md` for operational principles.

---

*Built with ❤️ by the SentinelAI Team.*
