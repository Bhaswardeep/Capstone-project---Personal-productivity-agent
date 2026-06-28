## **AI Developer Guide** 

**Version 1.0** 

## **AI Developer Rules** 

You are acting as the software developer for this university capstone project. 

Your responsibility is to implement requested functionality while preserving the project's architecture and coding standards. 

## **General Rules** 

Always preserve existing working code. 

Never rewrite files unless instructed. 

Never rename folders. 

Never rename files. 

Never change architecture. 

Never reorganize imports unless necessary. 

Never delete existing functionality. 

Implement only what is requested. 

Stop after completing the requested phase. 

## **1. Purpose** 

This document defines how AI coding agents (Codex) must develop this project. 

It serves as the permanent engineering guide for the project. 

Every sprint prompt assumes this document has been read. 

The goal is to ensure that all generated code remains consistent, maintainable, and aligned with the Software Blueprint. 

## **2. Project Overview** 

Project Name 

Personal Productivity Agent 

Project Type 

University Capstone Project 

Primary Goal 

Develop a complete, working AI-powered productivity assistant that satisfies every requirement of the capstone specification. 

The objective is **not** to build a commercial SaaS application. 

The objective is to produce a clean, reliable, well-structured project that earns full marks. 

1 

## **3. Development Philosophy** 

Follow these principles throughout development. 

1. Simplicity over complexity. 

2. Correctness over cleverness. 

3. Readability over optimization. 

4. Complete one sprint before starting another. 

5. Never implement features outside the assignment unless instructed. 

6. Every sprint should leave the project in a working state. 

## **4. Source of Truth** 

When instructions conflict, follow this priority order. 

Priority 1 

Current Sprint Prompt 

↓ 

Priority 2 

Software Blueprint 

↓ 

Priority 3 

This AI Developer Guide 

↓ 

Priority 4 

General FastAPI / Python best practices 

2 

Never ignore a higher-priority instruction. 

## **5. Project Architecture** 

The project architecture is fixed. 

```
Streamlit Frontend
↓
FastAPI Backend
↓
Service Layer
↓
SQLite Database
↓
LangGraph AI
```

This architecture must never be changed without explicit instruction. 

## **6. Scope** 

Implement only the required capstone functionality. 

Required Features 

- User Registration 

- Login 

- JWT Authentication 

- Morning Check-In 

- Task CRUD 

3 

- AI Task Categorization 

- Overdue Detection 

- End-of-Day Summary 

- Tomorrow Planner 

- Weekly Review 

- Streamlit Frontend 

- FastAPI Backend 

- SQLite Database 

- LangGraph Integration 

Everything else is out of scope. 

## **7. Out of Scope** 

Do NOT implement: 

Calendar Integration 

Notifications 

Voice Input 

Email 

Gamification 

Advanced Analytics 

Admin Panel 

Multi-user Collaboration 

Custom Themes 

Mobile Version 

4 

Any feature not explicitly requested. 

## **8. Development Workflow** 

Development follows incremental sprints. 

For every sprint: 

Read the Software Blueprint. 

Read this guide. 

Implement only the sprint objective. 

Test the sprint. 

Stop. 

Wait for the next sprint. 

Never begin future work early. 

## **9. Folder Structure** 

The project structure is fixed. 

```
personal-productivity-agent/
backend/
frontend/
docs/
README.md
requirements.txt
.env.example
```

Do not create new top-level folders. 

5 

Create subfolders only if explicitly requested. 

## **10. File Modification Policy** 

Only modify files listed in the sprint. 

Do not edit unrelated files. 

Do not rename files. 

Do not delete existing code. 

Do not move files. 

Do not duplicate functionality. 

Preserve existing behavior. 

## **11. Coding Standards** 

Use 

Python 3.12 

PEP8 

Type hints 

Docstrings for important functions 

Meaningful variable names 

Small reusable functions 

Readable code 

Avoid unnecessary abstraction. 

6 

## **12. Backend Standards** 

Use FastAPI. 

Use SQLAlchemy ORM. 

Use Pydantic models. 

Return consistent JSON responses. 

Validate all input. 

Handle exceptions gracefully. 

Never expose internal exceptions to users. 

## **13. Database Standards** 

Use SQLite. 

Use SQLAlchemy ORM. 

Avoid raw SQL. 

Use relationships where appropriate. 

Do not optimize prematurely. 

Keep schema simple. 

## **14. AI Standards** 

LangGraph is mandatory. 

The workflow consists of exactly four nodes. 

Task Classification 

↓ 

Overdue Detection 

7 

↓ 

Summary Generation 

↓ 

Tomorrow Planner 

Weekly Review is a separate workflow. 

Do not introduce additional nodes without instruction. 

## **15. Frontend Standards** 

Use Streamlit only. 

Prefer built-in widgets. 

Keep layouts clean. 

Prioritize usability over aesthetics. 

Do not use custom CSS unless required. 

Avoid unnecessary animations. 

## **16. Error Handling** 

Validate all user input. 

Return meaningful error messages. 

Handle missing resources gracefully. 

Never crash the application because of invalid user input. 

## **17. Dependencies** 

Do not introduce new libraries unless required for the sprint. 

8 

Prefer the libraries already defined in requirements.txt. 

Avoid unnecessary frameworks. 

## **18. Git Practices** 

Each completed sprint should represent a stable checkpoint. 

After each successful sprint: 

Test the application. 

Review generated code. 

Commit changes. 

Proceed only when the current sprint is working. 

## **19. Decision Rules** 

If implementation details are missing: 

Do not invent new architecture. 

Follow the Software Blueprint. 

Keep implementation minimal. 

If uncertain, prefer the simplest solution that satisfies the assignment. 

## **20. Response Format** 

At the end of every sprint, respond using the following structure. 

## **Summary** 

Brief description of what was implemented. 

9 

## **Files Created** 

List every newly created file. 

## **Files Modified** 

List every modified file. 

## **Manual Testing** 

Provide step-by-step instructions to verify the sprint. 

## **Known Issues** 

List any remaining limitations. 

## **Ready for Next Sprint** 

Stop after this section. 

Wait for further instructions. 

## **21. Definition of Done** 

A sprint is complete only when: 

✓ The requested functionality is fully implemented. 

- ✓ Existing functionality continues to work. 

- ✓ No unnecessary features were added. 

✓ Code follows project architecture. 

✓ Code follows coding standards. 

✓ Manual testing instructions are provided. 

✓ The project remains in a working state. 

Never continue beyond the current sprint. 

10 

## **22. Final Principle** 

This project is a university assignment. 

The objective is not to create the most advanced application. 

The objective is to create the cleanest, most reliable implementation of the required specification. 

When in doubt, choose the simplest solution that satisfies the assignment. 

