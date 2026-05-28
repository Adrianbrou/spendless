# Spendless

A personal finance tracker built to learn full stack development end to end. Log expenses, categorize them, filter by category, and see your monthly spending at a glance.

## Tech Stack

**Frontend**

- React (JSX)
- Vite
- Vanilla CSS
- Fetch API
**Backend**
- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic
- Postgres (dev and prod)
- Alembic (migrations)
- uv (package manager)
**Testing**
- pytest
- SQLite (in-memory, used only by the test suite for fast isolated runs)
**Tooling**
- GitHub Actions (CI)
- Git

## Project Structure

```
spendless/
├── .github/
│   └── workflows/          # CI pipelines (backend + frontend)
├── .gitignore
├── README.md
│
├── backend/
│   ├── pyproject.toml      # uv project config
│   ├── uv.lock
│   ├── main.py             # FastAPI app entry, mounts routers
│   ├── database.py         # SQLAlchemy engine and session
│   ├── models.py           # ORM models
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── alembic/            # migration scripts
│   ├── alembic.ini
│   ├── crud/               # raw DB operations, one file per resource
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   ├── income.py
│   │   ├── budget.py
│   │   └── subscription.py
│   ├── services/           # business logic, cross-table rules
│   │   ├── expense_service.py
│   │   ├── budget_service.py
│   │   └── subscription_service.py
│   └── routers/            # HTTP endpoints, one file per resource
│       ├── users.py
│       ├── categories.py
│       ├── expenses.py
│       ├── incomes.py
│       ├── budgets.py
│       └── subscriptions.py
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── App.css
        ├── api.js          # All fetch calls live here
        └── components/
            ├── ExpenseForm.jsx
            ├── ExpenseList.jsx
            ├── ExpenseItem.jsx
            ├── MonthlyTotal.jsx
            └── CategoryFilter.jsx
```

## Features

- Add an expense (amount, category, date, note)
- View all expenses in a list
- Delete an expense
- Filter expenses by category
- See total spent for the current month
- Persistent storage with Postgres

## Architecture

```
┌─────────────────────┐         HTTP          ┌──────────────────────┐
│   React Frontend    │  ─────────────────►   │   FastAPI Backend    │
│   (localhost:5173)  │  ◄─────────────────   │   (localhost:8000)   │
│                     │       JSON            │                      │
└─────────────────────┘                       └──────────┬───────────┘
                                                         │
                                                         ▼
                                              ┌──────────────────────┐
                                              │   Postgres           │
                                              └──────────────────────┘
```

**Layered backend pattern:** Router (HTTP) → Service (business logic) → CRUD (DB ops) → Database

## API Endpoints

| Method | Endpoint            | Description                |
| :----- | :------------------ | :------------------------- |
| POST   | `/expenses`         | Create a new expense       |
| GET    | `/expenses`         | List all expenses          |
| GET    | `/expenses/{id}`    | Get a single expense       |
| DELETE | `/expenses/{id}`    | Delete an expense          |
| GET    | `/summary/monthly`  | Total spent this month     |

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Backend Setup

```bash
cd backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App will be available at `http://localhost:5173`.

## Build Phases

1. **Backend Hello World**, FastAPI running, single route
2. **Backend Database**, Postgres + SQLAlchemy + Alembic, full model layer
3. **Backend CRUD layer**, raw DB operations per resource
4. **Backend Service layer**, business rules and cross-table logic
5. **Backend Routers**, POST / GET / PATCH / DELETE per resource, monthly summary
6. **Frontend Static UI**, React shell with hardcoded data
7. **Frontend Backend Wiring**, real fetch calls, state management
8. **Polish**, category filter, loading states, error handling, CI, pytest with SQLite in-memory

## Learning Goals

- HTML semantic structure and forms
- CSS layout (flexbox, responsive)
- JavaScript fundamentals (async, fetch, state)
- React component composition, hooks, props
- FastAPI routing, dependency injection, Pydantic validation
- SQLAlchemy ORM, sessions, migrations
- Layered backend architecture (router → service → crud)
- CORS, HTTP methods, JSON contracts
- GitHub Actions CI for a monorepo

## Author

Salomon Adrian Brou
