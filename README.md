# Personal Productivity Agent

Personal Productivity Agent is an AI-powered productivity application for planning daily work, managing tasks, reviewing progress, and generating intelligent productivity insights. It combines a FastAPI backend, Streamlit frontend, SQLite persistence, LangGraph workflow orchestration, and Groq-hosted LLM responses with automatic mock fallback.

## Live Demo

Frontend (Streamlit):
https://life-manager.streamlit.app/

Backend API:
https://personal-productivZity-agent-with-groq-ai.onrender.com/

Swagger Documentation:
https://personal-productivity-agent-with-groq-ai.onrender.com/docs

## Features

- JWT Authentication
- Task Management
- Dashboard
- Morning Check-In
- Evening Check-In
- Weekly Review
- LangGraph Workflow
- Groq AI Integration
- Automatic Mock AI Fallback
- FastAPI Backend
- Streamlit Frontend
- Swagger Documentation

## Technology Stack

- Frontend: Streamlit
- Backend: FastAPI
- Database: SQLite with SQLAlchemy
- Authentication: JWT with bcrypt password hashing
- AI: LangGraph, LangChain, Groq, deterministic mock fallback
- Deployment: Render for backend, Streamlit Community Cloud for frontend

## Project Structure

```text
backend/
frontend/
docs/
```

- `backend/`: FastAPI application, API routers, authentication, database models, services, and LangGraph AI workflow.
- `frontend/`: Streamlit pages for authentication, dashboard, tasks, check-ins, and weekly reviews.
- `docs/`: Project blueprint, AI developer guide, and development log.

## Installation

Clone the repository:

```bash
git clone https://github.com/Bhaswardeep/Capstone-project---Personal-productivity-agent
cd "Capstone-project---Personal-productivity-agent"
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
python -m uvicorn backend.main:app --reload
```

Run the frontend:

```bash
python -m streamlit run frontend/app.py
```

## Environment Variables

Create a local `.env` file from `.env.example` and configure the required values. The `.env` file is ignored by git and should not be committed.

- `GROQ_API_KEY`: Groq API key used for hosted LLM responses.
- `GROQ_MODEL`: Groq model name used by the AI service.
- `GROQ_TIMEOUT_SECONDS`: Timeout for Groq requests before falling back to mock AI.

## Database Schema

The database schema is implemented using SQLAlchemy ORM.

The complete schema can be found here:

- backend/models/models.py

GitHub link:
https://github.com/Bhaswardeep/Capstone-project---Personal-productivity-agent/blob/master/backend/models/models.py

## API Documentation

FastAPI provides Swagger documentation automatically after the backend starts:

Local:
http://127.0.0.1:8000/docs

Production:
https://personal-productivity-agent-with-groq-ai.onrender.com/docs

Use Swagger to inspect and test authentication, task, dashboard, check-in, and AI endpoints.

## AI Architecture

```text
Streamlit
-> FastAPI
-> LangGraph
-> Groq
-> Mock fallback
```

The frontend sends requests to FastAPI. The backend routes AI workflows through the LangGraph-based service layer. When Groq is configured and reachable, hosted LLM responses are returned. If Groq is unavailable or the API key is missing, the system automatically falls back to deterministic mock AI responses.

## Deployment

Backend:
- Render

Frontend:
- Streamlit Community Cloud

AI Provider:
- Groq API (llama-3.1-8b-instant)

If the Groq API is unavailable or the API key is missing, the application automatically falls back to the deterministic mock AI provider, ensuring uninterrupted functionality.

<!-- ## Screenshots

### Dashboard

### Tasks

### Morning Check-In

### Evening Check-In

### Weekly Review

### Swagger -->

<!-- ## Future Improvements

- Google Calendar integration
- Notifications
- Email reminders
- User analytics
- Multiple AI providers
- Export reports -->

## License

This project was developed as part of an academic capstone project.
