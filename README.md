# Personal Productivity Agent

An AI-powered productivity management application for planning daily work, tracking tasks, and generating productivity insights through a FastAPI backend, Streamlit frontend, SQLite persistence, and LangGraph-based AI workflows.

## Technology Stack

- Backend: FastAPI
- Frontend: Streamlit
- Database: SQLite
- ORM: SQLAlchemy
- Validation: Pydantic
- Authentication: JWT with bcrypt password hashing
- AI Orchestration: LangGraph and LangChain
- Environment Management: python-dotenv

## Folder Structure

```text
personal-productivity-agent/
backend/
  api/
  auth/
  database/
  models/
  schemas/
  services/
  langgraph/
  main.py
frontend/
  Login.py
  Register.py
  Dashboard.py
  Morning_Checkin.py
  Tasks.py
  Evening_Checkin.py
  Weekly_Review.py
docs/
README.md
requirements.txt
.env.example
.gitignore
```

## Local Setup

1. Create a virtual environment.
2. Activate the virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env`.
5. Fill in local environment values in `.env`.

## Run Instructions

Backend:

```bash
uvicorn backend.main:app --reload
```

Frontend:

```bash
streamlit run frontend/Dashboard.py
```
