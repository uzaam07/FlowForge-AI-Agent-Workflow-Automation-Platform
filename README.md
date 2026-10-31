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

## ✨ Features

### Workflow creation and management

- Create and save workflows through the workflow workspace.
- View and select existing workflows.
- Edit workflow details and configurations.
- Delete saved workflows with confirmation.
- Maintain organized workflow records.

### Workflow configuration and execution

- Configure workflows using the available workflow interface.
- Execute workflows through the backend workflow engine.
- Process workflow execution requests through FastAPI REST endpoints.
- Validate workflow data and configurations before processing.
- Capture workflow execution results and error information.

### Execution history and monitoring

- Track workflow execution records.
- View execution history for selected workflows.
- Display available execution statuses and results.
- Review previous workflow runs.
- Handle execution errors through backend response handling.

### Backend and API functionality

- FastAPI-powered REST API architecture.
- SQLAlchemy-based database operations.
- Pydantic request and data validation.
- Configurable database support for local and production environments.
- Authentication and security configuration.
- CORS configuration for controlled frontend-backend communication.

### User experience

- Interactive React and TypeScript frontend.
- Responsive workflow management interface.
- Dynamic workflow selection and updates.
- API-driven frontend and backend communication.
- Vite-powered frontend development and production builds.
- FastAPI health-check endpoint for backend availability.

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

## 🧠 Working Algorithm

### 1. Workflow creation and management

1. A user opens the FlowForge frontend and accesses the workflow workspace.
2. The user creates a new workflow by providing the required workflow details.
3. The React frontend sends the workflow data to the FastAPI backend through a REST API request.
4. The backend validates the incoming request using Pydantic schemas.
5. SQLAlchemy interacts with the database to store the workflow and its associated information.
6. The backend returns the saved workflow details, and the frontend updates the workflow list.
7. Users can view, modify, select, and delete their saved workflows.

### 2. Workflow configuration

1. A user selects an existing workflow from the workspace.
2. The frontend retrieves the workflow details from the backend.
3. The backend queries the database and returns the corresponding workflow data.
4. The user configures or modifies the workflow using the available workflow interface.
5. The frontend submits the updated configuration to the backend.
6. The backend validates the changes and updates the stored workflow through SQLAlchemy.
7. The updated workflow is returned to the frontend for display.

### 3. Workflow execution

1. A user initiates workflow execution from the frontend.
2. The frontend sends an execution request to the FastAPI backend, identifying the selected workflow.
3. The backend validates the request and retrieves the corresponding workflow configuration.
4. The workflow engine processes the workflow according to its defined execution logic.
5. The backend handles the execution process and captures the resulting output or error information.
6. The execution result is returned to the frontend through the API.
7. The frontend displays the execution status and relevant output to the user.

### 4. Execution history and result tracking

1. When a workflow execution is processed, the backend records the relevant execution information.
2. SQLAlchemy manages the interaction with the database to store execution records.
3. The frontend requests execution history for the selected workflow.
4. The backend retrieves the corresponding records from the database.
5. The API returns the execution history, including available status and result information.
6. The frontend displays the execution records, allowing users to review previous workflow runs.

### 5. Backend API and security flow

1. The frontend communicates with the backend through configured REST API endpoints.
2. FastAPI receives incoming requests and validates their structure.
3. The backend applies the configured authentication and security checks where required.
4. Application logic processes authorized requests and interacts with the database.
5. The backend returns structured responses or appropriate error messages.
6. CORS configuration controls which frontend origins are permitted to access the backend API.

> **Execution note:** Workflow execution is handled by the backend workflow engine. The actual operations depend on the workflow configuration and execution logic implemented in the application. External integrations, distributed execution, and background job processing should only be documented as supported once they are implemented.

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
