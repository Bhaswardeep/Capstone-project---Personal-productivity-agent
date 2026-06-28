## Personal Productivity Agent 

Software Blueprint & Architecture Document Version 1.0 

## 1. Executive Summary 

## 1.1 Overview 

The Personal Productivity Agent is an AI-powered productivity management application designed to help users organize daily work, monitor progress, identify overdue tasks, and generate intelligent summaries and action plans. 

Unlike traditional to-do list applications, this system utilizes a Large Language Model (LLM) together with LangGraph to maintain contextual memory and assist users during both morning planning and end-of-day reflection. 

The application combines modern backend technologies with AI orchestration to create an intelligent productivity assistant capable of remembering historical context and generating personalized recommendations. 

The project satisfies all required outcomes specified in the capstone while extending the experience into a portfolio-quality application. 

## 2. Problem Statement 

Most productivity applications only store tasks. 

They do not understand: 

- what the user accomplished 

- what was postponed 

- recurring productivity patterns 

- why tasks keep slipping 

- how tomorrow should be planned 

Users frequently: 

- forget unfinished work 

- underestimate priorities 

- lose track of recurring tasks 

- struggle to review previous weeks 

This project solves those problems using AI. 

Instead of acting as a passive task manager, the application becomes an active productivity coach that learns from previous check-ins and assists the user in planning future work. 

## 3. Project Objectives 

The system aims to: 

- Manage daily tasks 

- Track task completion 

- Classify tasks automatically 

- Detect overdue tasks 

- Generate intelligent End-of-Day summaries 

- Recommend tomorrow’s work plan 

- Detect long-term productivity patterns 

- Maintain conversation history using LangGraph state 

- Provide a clean, modern productivity dashboard 

## 4. Project Scope 

## Included 

- ✓ User authentication 

- ✓ Morning check-in 

- ✓ Evening check-in 

- ✓ AI task categorization 

- ✓ Priority management 

- ✓ Due dates 

- ✓ Overdue detection 

- ✓ Daily summaries 

- ✓ Tomorrow planning 

- ✓ Weekly reviews 

- ✓ Productivity dashboard 

- ✓ Statistics 

- ✓ User profile 

- ✓ LangGraph memory 

- ✓ SQLite persistence 

- ✓ Streamlit frontend 

- ✓ FastAPI backend 

## 5. Target Users 

The application is intended for: 

- Students 

- Software developers 

- Researchers 

- Office workers 

- Freelancers 

- Anyone wanting AI-assisted productivity management 

## 6. Technology Stack 

Frontend 

Streamlit 

Reason: 

- Fast development 

- Beautiful widgets 

- Native forms 

- Excellent dashboard support 

- Easy deployment 

## Backend 

## FastAPI 

Reason: 

- Extremely fast 

- Automatic Swagger documentation 

- JWT support 

- Easy API creation 

- Async capable 

## Database 

SQLite 

Reason: 

- Zero configuration 

- Lightweight 

- Perfect for solo capstone 

- SQLAlchemy support 

## ORM 

## SQLAlchemy 

Reasons 

- Clean models 

- Easy migrations 

- Relationship support 

## Authentication 

JWT 

Password hashing using bcrypt 

OAuth2PasswordBearer 

## AI 

LangGraph 

Groq/OpenAI/Ollama compatible 

One persistent thread per user 

## Deployment 

Frontend 

Streamlit Community Cloud 

Backend 

Render 

## 7. Overall System Architecture 

The application follows a layered architecture. 

```
                User
```

│ 

```
          Streamlit Frontend
```

│ 

```
          HTTP REST Requests
```

│ 

```
            FastAPI Backend
```

┌───────────┴───────────┐ 

```
 Authentication         AI Services
```

│ │ 

```
 Task Services        LangGraph Agent
```

│ │ 

```
 Database Layer       LLM Provider
```

│ 

```
SQLite + SQLAlchemy
```

This separation ensures that each layer has a single responsibility. 

## 8. Application Workflow 

## Morning 

User logs in 

## ↓ 

Dashboard opens 

## ↓ 

Morning Check-in 

## ↓ 

Create today’s tasks 

## ↓ 

AI categorizes tasks 

## ↓ 

Database updated 

- ↓ 

## Dashboard refreshed 

## Evening 

User opens Evening Check-in 

## ↓ 

Marks completed tasks 

## ↓ 

Adds notes 

## ↓ 

AI detects overdue work 

## ↓ 

LangGraph generates summary 

## ↓ 

Tomorrow plan generated 

## ↓ 

Everything saved 

## Weekly 

Scheduler triggers 

## ↓ 

Read last seven days 

## ↓ 

Identify patterns 

## ↓ 

Generate weekly review 

## ↓ 

Store report 

↓ 

Display on dashboard 

## 9. Core Features 

## Authentication 

Register 

Login 

Logout 

JWT tokens 

Password hashing 

Remember session 

## Dashboard 

Today's Tasks 

Overdue Tasks 

Latest AI Summary 

Quick Actions 

## Morning Check-In 

Today’s goals 

Task title 

Description 

Priority 

Due date 

Estimated duration 

AI Notes 

## Save tasks 

## Task Management 

Create task Update task 

Delete task 

Complete task 

Reopen task 

Change priority 

Change due date 

Filter 

Search 

Sort 

## AI Categorization 

Automatically classify every task into 

Work 

Personal 

Health 

Learning 

Other 

AI also estimates urgency: 

Low 

Medium 

High 

Critical 

## Overdue Detection 

Daily automatic check 

Highlight overdue tasks 

Show number overdue 

Suggest highest priority overdue work 

## Evening Check-In 

Completed tasks Unexpected work 

Daily notes 

Mood 

Energy level Challenges Wins 

## AI End-of-Day Summary 

Generated automatically. 

Example 

Today you completed 7 out of 10 planned tasks. Most progress was made on work-related activities. Two learning tasks remain incomplete and have been recommended for tomorrow. Overall productivity remained high despite several interruptions. 

## Tomorrow Planner 

AI generates 

Top priorities Carry-forward tasks 

Suggested schedule 

## Estimated workload 

## Focus recommendation 

## Weekly Review 

Charts 

Task completion rate Category distribution Most productive day Repeated postponements Recommendations 

## 10. Functional Requirements 

FR-01 User registration 

FR-02 User login 

FR-03 JWT authentication 

FR-04 Create task 

FR-05 Update task FR-06 Delete task 

FR-07 Complete task FR-08 Morning check-in FR-09 Evening check-in FR-10 AI categorization FR-11 Overdue detection FR-12 Daily summaries FR-13 Tomorrow planning FR-14 Weekly review FR-15 Dashboard analytics 

## 11. Non-Functional Requirements 

Fast response time 

Simple UI 

Secure authentication 

Scalable architecture 

Maintainable code 

Modular backend 

Reusable services 

Responsive dashboard 

Clean documentation 

## 12. Success Criteria 

The project will be considered complete when: 

- ✓ Users can authenticate. 

- ✓ Morning and evening check-ins work. 

- ✓ Tasks are stored correctly. 

- ✓ AI classifies tasks. 

- ✓ Overdue tasks are detected. 

- ✓ End-of-Day summaries are generated. 

- ✓ Tomorrow plans are generated. 

- ✓ Weekly reviews are generated. 

- ✓ Dashboard updates automatically. 

- ✓ Project deploys successfully. 

End of Part 1 

The next part of this document will include: 

- Complete folder structure 

- Database schema 

- SQLAlchemy model design 

- API specification 

- Streamlit page layouts 

- LangGraph architecture 

- Detailed AI workflow 

- Security architecture 

- Deployment architecture 

## Personal Productivity Agent 

## — Part 2 System Design & Software Architecture 

## 13. Overall Software Architecture 

The application follows a Layered Architecture with clear separation of responsibilities. 

User 

│ 

Streamlit Frontend 

│ 

REST API (HTTP) 

│ 

FastAPI Backend 

**==> picture [305 x 223] intentionally omitted <==**

**----- Start of picture text -----**<br>
                  │<br> ┌────────────────┼────────────────┐<br> │                │                │<br>Auth Layer   Task Service    AI Service<br> │                │                │<br> │           SQLAlchemy      LangGraph<br> │                │                │<br> └────────────────┼────────────────┘<br>                  │<br>             SQLite Database<br>**----- End of picture text -----**<br>


Each layer has only one responsibility. 

- Frontend only displays data. 

- Backend handles business logic. 

- AI service generates intelligent outputs. 

- Database stores application state. 

This makes the project easier to maintain, debug, and extend. 

## 14. Project Folder Structure 

personal-productivity-agent/ 

│ ├── backend/ │   │ │   ├── app/ │   │ │   ├── api/ 

│   │     auth.py │   │     tasks.py 

- │   │     dashboard.py 

- │   │     ai.py 

- │   │ 

- │   ├── core/ 

- │   │     config.py 

- │   │     security.py 

│   │ 

│   ├── database/ 

│   │     database.py 

│   │     models.py 

- │   │     schemas.py 

- │   │ 

- │   ├── services/ 

│   │     auth_service.py 

│   │     task_service.py 

│   │     ai_service.py │   │ 

│   ├── langgraph/ 

│   │     graph.py 

│   │     nodes.py 

│   │     state.py │   │ 

│   ├── utils/ │   │ │   ├── main.py │   │ 

│   └── requirements.txt 

│ 

├── frontend/ 

│ 

│   dashboard.py 

│ 

│   pages/ 

│ 

│       Login.py 

│       Register.py 

│       Dashboard.py 

│       Morning_Checkin.py 

│       Evening_Checkin.py 

│       Tasks.py 

│       Weekly_Review.py 

│       Settings.py 

│ 

├── database/ 

│ 

│   productivity.db 

│ 

├── docs/ 

│ 

│   blueprint.pdf 

│ 

├── README.md 

│ 

└── .env 

## 15. Why This Structure? 

Many student projects place all FastAPI routes inside one file. 

That quickly becomes difficult to maintain. 

Instead we separate: 

API Layer ↓ 

Service Layer ↓ Database Layer ↓ AI Layer 

Each layer only knows about the layer below it. 

This is a professional architecture used in production systems. 

## 16. Database Design 

The application only needs five core tables. 

Users 

↓ Tasks 

↓ 

DailyLogs 

↓ 

EODSummaries 

↓ 

WeeklyReviews 

This keeps the database simple while satisfying every project requirement. 

## 17. Database Schema 

## USERS 

Stores registered users. 

Columns 

id 

username 

email 

hashed_password 

created_at 

last_login 

## TASKS 

Stores every task. 

Columns 

id 

user_id 

title 

description category priority status due_date estimated_minutes completed_at created_at updated_at 

Status values 

Pending 

In Progress Completed Cancelled 

Category values 

Work 

Learning Health 

Personal Other 

Priority values 

Low 

Medium 

High 

Critical 

## DAILY LOGS 

Stores user reflections. 

Columns 

id 

user_id 

date 

morning_notes evening_notes energy_level 

mood 

wins 

challenges created_at 

## EOD SUMMARIES 

Stores AI-generated summaries. 

Columns 

id 

user_id 

date 

summary 

tomorrow_plan 

created_at 

## WEEKLY REVIEWS 

Stores weekly AI analysis. 

Columns 

id 

user_id 

week_start 

week_end 

review 

productivity_score 

patterns 

recommendations 

created_at 

## 18. Database Relationships 

User 

│ 

├── Tasks 

│ 

├── Daily Logs 

│ 

├── EOD Summaries 

│ 

- └── Weekly Reviews 

One user owns everything. 

No shared resources. 

No complicated joins. 

## 19. Backend Modules 

Instead of putting everything into FastAPI routes, responsibilities are divided. 

## Auth Service 

Register 

Login 

JWT 

Password hashing 

Token verification 

## Task Service 

Create task 

Update task 

Delete task 

Complete task 

Search 

Filtering 

Statistics 

## Dashboard Service 

Today's progress 

Weekly progress 

Charts 

Upcoming tasks 

Overdue tasks 

Statistics 

## AI Service 

Task classification 

Summary generation Tomorrow planning 

Weekly insights 

LLM communication 

## 20. Streamlit Page Design 

Instead of only implementing the required pages, the application should feel like a polished productivity app. 

## Login 

Email 

Password 

Login Button 

Register Link 

## Register 

Username 

Email 

Password 

Confirm Password 

Create Account 

## Dashboard 

This is the application's home page. 

Sections 

Today's Progress 

Task Statistics 

Overdue Tasks Upcoming Tasks 

Recent AI Summary 

Quick Actions 

Productivity Score 

Navigation Sidebar 

## Morning Check-In 

Fields 

Today's Goal 

Task Entry 

Priority 

Due Date 

Estimated Time 

Notes 

AI Suggestions 

Save Button 

## Tasks Page 

Task Table 

Filters 

Search 

Status 

Priority 

Category 

Sorting 

Quick Complete Button 

Edit 

Delete 

## Evening Check-In 

Completed Tasks 

Unexpected Tasks 

Wins 

Challenges 

Mood 

Energy 

Generate Summary Button 

## Weekly Review 

Charts 

Completion % 

Category Breakdown 

Overdue Trends 

Repeated Tasks 

AI Insights 

## Recommendations 

## 21. Navigation Flow 

Login 

↓ 

Dashboard 

↓ 

Morning Check-In 

↓ 

Tasks 

↓ 

Evening Check-In 

↓ 

Dashboard 

↓ 

## Weekly Review 

Every screen is accessible from the sidebar. 

## 22. Dashboard Layout 

------------------------------------------------- 

Logo 

------------------------------------------------- 

Today's Progress 

------------------------------------------------- 

Task Statistics 

------------------------------------------------- 

Upcoming Tasks 

------------------------------------------------- 

Overdue Tasks 

------------------------------------------------- 

Recent AI Summary 

------------------------------------------------- 

Quick Actions 

------------------------------------------------- 

Productivity Score 

------------------------------------------------- 

## 23. Why This Design? 

This layout ensures the dashboard immediately answers: What should I do today? 

↓ 

What is overdue? 

↓ 

How productive am I? 

↓ 

What did AI recommend? 

↓ 

What should I work on next? 

The user never has to navigate multiple pages to understand their day. 

End of Part 2 

The next section will cover: 

- FastAPI endpoint design 

- Complete API specification 

- LangGraph architecture 

- AI node design 

- Prompt engineering strategy 

- LLM workflow 

- Memory management 

- Scheduler design 

These sections define the application's "brain" and will directly guide the implementation of the AI functionality. 

## Personal Productivity Agent 

– Part 3 Backend Architecture, AI Design & API Specification 

## 24. Backend Philosophy 

The backend should not be a collection of API endpoints that directly manipulate the database. 

Instead, every request should follow the same architecture. 

Frontend │ REST API │ FastAPI Router │ Service Layer │ Database / AI Layer │ SQLite / LangGraph 

This architecture keeps every component independent. 

If the frontend changes tomorrow, the backend does not. 

If the database changes tomorrow, the API does not. 

## 25. Backend Modules 

The backend will contain six major modules. 

## – Module 1 Authentication 

Responsibilities 

- Register users 

- Login users 

- JWT creation 

- Password hashing 

- Token verification 

- Protected routes 

## – Module 2 Task Management 

## Responsibilities 

- Create tasks 

- Edit tasks 

- Delete tasks 

- Mark complete 

- Reopen tasks 

- Search 

- Filtering 

- Statistics 

## – Module 3 Dashboard 

## Responsibilities 

Calculate 

Today's Progress 

Completion % 

Pending Tasks 

Overdue Tasks 

Upcoming Tasks 

Weekly Statistics 

Productivity Score 

## – Module 4 AI Service 

This module communicates with the LLM. 

Responsibilities 

Task Classification 

Priority Detection 

EOD Summary 

Tomorrow Planner 

Weekly Review 

Prompt Management 

Model Selection 

## – Module 5 LangGraph 

Responsible for AI orchestration. 

Contains 

Graph 

Nodes 

State 

Memory 

Checkpointer 

## Scheduler 

Make a button in Streamlit: 

Generate Weekly Review 

When clicked: 

Frontend 

↓ 

FastAPI 

↓ LangGraph ↓ Weekly Review ↓ 

Save to Database 

## 26. FastAPI Endpoint Design 

Authentication 

POST   /auth/register 

POST   /auth/login 

GET    /auth/me 

Dashboard 

GET    /dashboard 

## GET    /dashboard/statistics 

Tasks 

GET     /tasks 

POST    /tasks 

PUT     /tasks/{id} 

DELETE  /tasks/{id} 

PATCH   /tasks/{id}/complete 

PATCH   /tasks/{id}/reopen 

Morning Check-in POST /checkin/morning 

Evening Check-in POST /checkin/evening 

AI 

POST /ai/eod 

POST /ai/tomorrow 

POST /ai/classify 

POST /ai/weekly-review 

Weekly Review 

GET /weekly 

GET /weekly/latest 

## 27. Request Lifecycle 

Every API request follows the same sequence. 

Frontend 

↓ 

FastAPI Route 

↓ 

Authentication 

↓ 

Validation 

↓ 

Business Logic 

↓ 

Database 

↓ 

Response 

↓ 

Frontend 

AI endpoints simply add another step. 

Validation 

↓ 

Database 

↓ 

LangGraph 

↓ 

LLM 

↓ 

Database 

↓ 

Response 

## 28. LangGraph Architecture 

Rather than writing one huge AI function, we separate every responsibility into its own node. 

START 

↓ 

Classifier Node 

↓ 

Overdue Node 

↓ 

Summary Node 

↓ 

Tomorrow Planner 

↓ 

END 

This makes debugging much easier. 

## 29. LangGraph State 

The graph shares one state object. 

User ID 

Today's Tasks 

Completed Tasks 

Pending Tasks 

Overdue Tasks 

Daily Notes 

AI Category Results 

Summary 

Tomorrow Plan 

Weekly Context 

Every node only edits the fields it owns. 

## 30. AI Nodes 

## Node 1 

Task Classifier 

Input 

Tasks 

Output 

Category 

Priority 

Urgency 

Purpose 

Automatically classify every task. 

## Node 2 

Overdue Analyzer 

Input 

Tasks 

Current Date 

Output 

Overdue Tasks 

Critical Tasks 

Suggested Priority 

Purpose 

Detect unfinished work. 

## Node 3 

Summary Generator 

Input 

Today's Activity 

Output 

End-of-Day Summary 

Purpose 

Generate readable summary. 

## Node 4 

Tomorrow Planner 

Input 

Summary 

Overdue Tasks 

Priorities 

Output 

Tomorrow Plan 

Purpose 

Generate tomorrow's schedule. 

## Node 5 

Weekly Reviewer 

Runs every Sunday. 

Input 

Previous Seven Days 

Output 

Weekly Review 

Patterns 

Recommendations 

Purpose 

Long-term analysis. 

## 31. AI Prompt Design 

Every node owns one prompt. 

Never build giant prompts. 

Example 

Classifier Prompt 

↓ 

Summary Prompt 

↓ 

Tomorrow Prompt 

↓ 

Weekly Prompt 

Each prompt has only one responsibility. 

This dramatically improves LLM quality. 

## 32. LLM Strategy 

Not every task requires the most powerful model. 

Simple tasks 

↓ 

Small model 

Complex reasoning 

↓ 

Large model 

Recommended strategy 

Classifier 

Fast inexpensive model 

Summary 

Better reasoning model 

Tomorrow Planner 

Better reasoning model 

Weekly Review 

Best available model 

This keeps API costs low while maintaining quality. 

## 33. Memory Design 

The application has two types of memory. 

Short-Term Memory 

Current LangGraph state. 

Long-Term Memory 

SQLite database. 

The graph only remembers today's workflow. 

The database remembers everything. 

## 35. AI Service Workflow 

When the user clicks 

Run My End-of-Day 

the following happens. 

User 

↓ 

FastAPI 

## ↓ 

Load Today's Tasks 

↓ 

LangGraph Starts 

↓ 

Classify Tasks 

↓ 

Detect Overdue 

## ↓ 

Generate Summary 

## ↓ 

Generate Tomorrow Plan 

↓ 

Save Summary 

↓ 

Return Response 

## ↓ 

Dashboard Refreshes 

## 36. Weekly Review Workflow 

Every Sunday 

Scheduler Starts 

↓ 

Load Last 7 Days 

↓ 

Calculate Statistics 

↓ 

LLM Finds Patterns 

↓ Generate Review 

↓ 

Save Review 

↓ 

Dashboard Updates 

## 37. Error Handling 

Every endpoint returns a consistent format. 

Success 

{ 

"success": true, 

"message": "Task created successfully.", 

"data": { } 

} 

Failure 

{ 

"success": false, 

"message": "Task not found.", 

"error": "TASK_NOT_FOUND" 

} 

Never return inconsistent responses. 

## 38. Logging Strategy 

The application uses lightweight logging primarily for debugging during development. 

The backend logs: 

- User authentication events 

- Database errors 

- AI request failures 

- Unexpected exceptions 

Python's built-in logging module will be used for backend logging. 

Complex logging systems are unnecessary for this capstone project. 

## 39. Security 

JWT Authentication 

Password Hashing 

Protected Routes 

Input Validation 

Environment Variables 

No API keys inside code 

Never trust frontend input. 

Always validate inside FastAPI. 

## 41. Architecture Summary 

The application follows a clean, modular architecture. 

Streamlit 

↓ 

FastAPI 

↓ 

Service Layer 

↓ 

LangGraph 

↓ 

SQLite 

↓ 

LLM 

Each component has one responsibility. 

The result is a project that is: 

- ✓ Easy to extend 

- ✓ Easy to debug 

- ✓ Easy to deploy 

- ✓ Portfolio quality 

End of Part 3 

The next section will cover: 

- Complete UI/UX design 

- Every Streamlit page 

- Widget layouts 

- Dashboard wireframes 

- User experience flow 

- Productivity analytics 

- Color palette 

- Design consistency 

- Future scalability 

## – Part 4 User Interface & User Experience Blueprint 

## 42. UI Philosophy 

The interface should prioritize simplicity over visual complexity. 

The user should always know: 

- What needs to be done today 

- What is overdue 

- What has already been completed 

- What AI recommends next 

The application should require as few clicks as possible. 

## 43. Navigation Structure 

The application contains seven pages. 

Login 

↓ 

Register ↓ Dashboard ↓ Morning Check-In 

↓ 

Tasks 

↓ Evening Check-In 

↓ Weekly Review 

Navigation is provided through the Streamlit sidebar. 

## 44. Login Page 

Components 

- Email 

- Password 

- Login Button 

- Register Link 

Purpose 

Authenticate users using JWT. 

## 45. Register Page 

Components 

Username 

Email 

Password 

Confirm Password 

Register Button 

Purpose 

Create a new user account. 

## 46. Dashboard 

The dashboard is the application's home page. 

Layout 

------------------------------------------------ 

Welcome User 

------------------------------------------------ 

## Today's Progress 

------------------------------------------------ 

Today's Tasks 

------------------------------------------------ 

Overdue Tasks 

------------------------------------------------ 

Latest AI Summary 

------------------------------------------------ 

Quick Actions 

Morning Check-in 

Evening Check-in 

Generate Weekly Review 

------------------------------------------------ 

## 47. Morning Check-In 

Purpose 

Plan today's work. 

Components 

Today's Goal 

Task Title 

Task Description 

Priority 

Due Date 

Estimated Duration 

Save Task Button 

AI Categorize Button 

## 48. Tasks Page 

Displays every task. 

Columns 

Title Category Priority Status Due Date Actions Buttons Complete Edit Delete Filters Category Status Priority Search 

## 49. Evening Check-In 

Purpose 

Reflect on today's work. 

Components 

Completed Tasks 

Wins 

Challenges Daily Notes 

Generate Summary Button 

The AI generates: 

- End-of-Day Summary 

- Tomorrow Plan 

## 50. Weekly Review 

Purpose 

Generate AI review of the previous week. 

Components 

Generate Weekly Review Button 

Weekly Review 

Recommendations 

Patterns 

Completion Percentage 

## 51. Design Principles 

Keep pages uncluttered. 

Use Streamlit containers. 

Use expandable sections only where helpful. 

Avoid unnecessary animations. 

Focus on readability. 

