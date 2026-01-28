# 🛡️ SentinelAI

SentinelAI is a state-of-the-art, AI-powered study-abroad counselling platform designed to guide students through the complexities of international education. By leveraging advanced LLMs and a deterministic execution architecture, SentinelAI provides personalized recommendations, application guidance, and a persistent AI counsellor.

---

## 🚀 Key Features

- **🧠 Smart Onboarding**: Mandatory profiling to understand academic background, study goals, budget, and readiness.
- **📊 Interactive Dashboard**: A central hub to track profile strength, current stages, and AI-generated to-do lists.
- **🤖 AI Counsellor (Core)**: A persistent AI agent powered by Groq that recommends universities (Dream/Target/Safe), explains fit/risks, and performs actions on behalf of the user.
- **🎓 University Locking**: A strategic flow where students shortlist and lock-in target universities to unlock specific application guidance.
- **✅ Application Guidance**: Automated generation of timelines, document checklists, and task tracking for SOPs and exams.

---

## 🏗️ Project Structure

SentinelAI is organized as a monorepo with a 3-layer architecture for maximum reliability.

- **/frontend**: A polished Next.js application built with TypeScript and Bun. Uses Clerk for authentication and provides a premium UI/UX.
- **/backend**: A high-performance FastAPI service that handles core logic, AI orchestration, and data management. Uses `uv` for dependency management.
- **/directives**: Contains Standard Operating Procedures (SOPs) in Markdown that define how the AI agent operates.
- **/execution**: (Located within backend context) Deterministic Python scripts that interface with APIs and databases.

---

## 🛠️ Tech Stack

### Frontend

- **Framework**: Next.js 15+ (App Router)
- **Runtime**: Bun
- **Authentication**: Clerk
- **Styling**: Vanilla CSS / Modern UI components
- **State Management**: React Hooks

### Backend

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **AI Engine**: Groq (LLM Orchestration)
- **Dependency Management**: `uv`
- **Validation**: Pydantic v2

---

## 🚦 Getting Started

### 1. Prerequisites

- **Bun** (for frontend)
- **Python 3.11+** and **uv** (for backend)
- **API Keys**: Clerk (Frontend/Backend) and Groq (Backend)

### 2. Backend Setup

```bash
cd backend
uv sync
# Copy .env.example to .env and fill in your keys
uv run uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
bun install
# Copy .env.example to .env.local and fill in your Clerk keys
bun dev
```

---

## 📜 Architecture: The 3-Layer System

As outlined in `AGENTS.md`, this project follows a strict separation of concerns:

1. **Layer 1: Directive (What to do)** - SOPs in `directives/` define the goals.
2. **Layer 2: Orchestration (Decision making)** - The AI agent routes requests and handles errors.
3. **Layer 3: Execution (Doing the work)** - Deterministic scripts in `execution/` handle the actual work.

---

## 🤝 Contributing

This project is built with a focus on modularity ("one feature, one file"). Please refer to `PLAN.md` for the core prototype flow and `AGENTS.md` for operational principles.

---

*Built with ❤️ by the SentinelAI Team.*
