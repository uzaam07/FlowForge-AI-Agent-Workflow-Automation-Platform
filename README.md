# FlowForge AI — AI Agent Workflow Automation Platform

A full-stack workflow automation platform built with **FastAPI, SQLAlchemy, React, TypeScript, and Vite**. FlowForge provides a visual workspace for creating, managing, and executing workflows through an interactive interface and REST API.

## 🚀 Live Demo

- **Frontend:** https://flowforge-ai-e7nl.onrender.com
- **Backend API:** https://flowforge-ai-api-o1x2.onrender.com

> **Important — activate the backend first:** The backend runs on a free hosting service and may sleep after inactivity. First open the [Backend API](https://flowforge-ai-api-o1x2.onrender.com/) and wait for it to respond. Then open the [Frontend](https://flowforge-ai-e7nl.onrender.com/) and use the application. The first request may take a little while while the backend wakes up. Authentication and workspace features require both services to be available

## ✨ Overview

**FlowForge AI** is a full-stack workflow automation application designed to simplify the creation, organization, and execution of automated workflows.

The platform combines a React-based frontend with a FastAPI backend, providing an interactive environment for managing workflows and communicating with backend services through REST APIs.

It is designed as a portfolio-ready software engineering project demonstrating full-stack development, API integration, database management, backend architecture, and workflow execution.

## 🛠️ Features

- **Visual Workflow Workspace** — Interactive interface for creating and managing workflows.
- **Workflow Management** — Create, view, update, and delete saved workflows.
- **Workflow Execution** — Execute workflows through the backend workflow engine.
- **Execution History** — View workflow execution records and their results.
- **REST API Integration** — Frontend communicates with backend services through API endpoints.
- **Persistent Data Storage** — SQLAlchemy-based database integration for application data.
- **Responsive Interface** — Modern interface designed for a clean workflow management experience.
- **Backend Validation** — Structured request validation and application-level error handling.
- **Authentication and Security** — Backend security configuration and protected application functionality.
- **Automated Testing** — Backend test suite covering core application functionality.

## 💻 Tech Stack

| Layer / Category | Technologies | Purpose |
|---|---|---|
| **Frontend** | React, TypeScript | Build the interactive user interface and manage application components with type safety. |
| **Build Tool** | Vite | Provide fast development server startup and optimized frontend production builds. |
| **Styling** | CSS | Design the application layout, visual components, and responsive interface. |
| **Backend** | Python, FastAPI | Develop backend services, handle application logic, and expose REST API endpoints. |
| **API Server** | Uvicorn | Run and serve the FastAPI application. |
| **Database** | SQLite, PostgreSQL | Store application data during local development and production deployment. |
| **ORM** | SQLAlchemy | Manage database models, queries, and database interactions using Python. |
| **Data Validation** | Pydantic | Validate incoming API requests and structure application data. |
| **Authentication & Security** | Backend security configuration | Handle authentication-related functionality, application security, and request protection. |
| **Testing** | Pytest | Test backend functionality and verify application behavior. |
| **Deployment** | Render | Host and deploy the frontend and backend services. |
| **Database Hosting** | Neon PostgreSQL | Provide managed PostgreSQL database hosting for production. |
| **Version Control** | Git, GitHub | Track source-code changes and manage the project repository. |
| **Development Environment** | Visual Studio Code, npm | Support application development, dependency management, and frontend workflows. |

## 📂 Project Structure

```text
flowforge-ai/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   └── workflow_engine.py
│   │
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   ├── main.tsx
│   │   └── styles.css
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

## ⚙️ Run Locally

### Prerequisites

- Python 3.11+
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/uzaam07/flowforge-ai.git
cd flowforge-ai
```

### 2. Set Up the Backend

```bash
cd backend

python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Set Up the Frontend

Open a separate terminal:

```bash
cd frontend
npm install
```

Create a frontend environment file named `.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the development server:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

### 4. Build the Frontend

To generate a production build:

```bash
npm run build
```

The generated production files are placed inside the `dist/` directory.

## 🧪 Backend Testing

FlowForge includes a backend test suite to validate core application functionality.

Run the tests from the backend directory:

```bash
python -m pytest -q
```

The test suite was verified with:

```text
8 passed, 1 warning
```

The warning was related to a Starlette/httpx deprecation and did not affect the test results.

## 🌐 Deployment

FlowForge AI is deployed using **Render**.

The frontend and backend are hosted as separate services.

| Component | Deployment |
|---|---|
| Frontend | Render Static Site |
| Backend | Render Web Service |
| Database | Configurable database connection |

### Production Environment Variables

Configure the appropriate environment variables in your deployment provider.

**Backend:**

```env
APP_ENV=production
DEBUG=false
SECRET_KEY=your-secure-secret-key
DATABASE_URL=your-database-connection-string
CORS_ORIGINS=https://your-frontend-domain
TRUSTED_HOSTS=your-backend-domain
```

**Frontend:**

```env
VITE_API_BASE_URL=https://your-backend-domain
```

Never commit production secrets, `.env` files, virtual environments, local databases, or generated build directories to GitHub.


## 🎯 Project Goals

This project demonstrates practical experience in:

- Full-stack application development.
- REST API design and integration.
- Backend development using FastAPI.
- Database modelling and ORM integration.
- Workflow execution and application architecture.
- Frontend development using React and TypeScript.
- Environment-based configuration and deployment.
- Automated backend testing.

## 👨‍💻 Author

- **Name:** Uzaam Shaad K
- **GitHub:** [uzaam07](https://github.com/uzaam07)
- **Portfolio:** [uzaam07.github.io](https://uzaam07.github.io/Portfolio/)
- **LinkedIn:** [linkedin.com/in/uzaamshaad](https://linkedin.com/in/uzaamshaad)

---

⭐ If you find this project interesting, consider giving the repository a star!
