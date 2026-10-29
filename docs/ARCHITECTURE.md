# Architecture

```text
React + TypeScript / React Flow
       | JSON API + bearer token
       v
FastAPI routes and auth dependencies
       |-- account-scoped workflow queries
       |-- schema and directed-acyclic-graph validation
       |-- bounded deterministic workflow executor
       v
SQLAlchemy ORM
       v
PostgreSQL (Docker / production) or SQLite (local)
```

The MVP executes a validated graph in topological order and stores step-level output for inspection. External HTTP actions and arbitrary code execution are intentionally disabled. The AI summary step is a deterministic demo implementation.
