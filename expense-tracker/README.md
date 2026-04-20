# ExpenseTracker — Industry Standard Full Stack App

Built by Ayush Meshram | Python · FastAPI · Next.js · MongoDB · Redis · Docker · AI

## Stack
- **Backend:** FastAPI (Python), JWT Auth, MongoDB, Redis cache
- **Frontend:** Next.js, TailwindCSS
- **AI:** Claude API (financial advice)
- **DevOps:** Docker, Nginx, GitHub Actions CI/CD

## Run locally (one command)
```bash
docker-compose up --build
```

Then open:
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs

## Project structure
```
expense-tracker/
├── backend/
│   └── app/
│       ├── core/        # config, db, redis, security
│       ├── models/      # MongoDB document models
│       ├── schemas/     # Pydantic request/response schemas
│       ├── services/    # business logic, AI service
│       ├── routers/     # API route handlers
│       └── tests/       # pytest tests
├── frontend/
│   └── src/
│       ├── components/  # React components
│       ├── context/     # Auth context
│       ├── hooks/       # Custom React hooks
│       └── utils/       # API utility
├── nginx/               # Reverse proxy config
├── .github/workflows/   # CI/CD pipeline
└── docker-compose.yml   # Run everything
```

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| POST | /api/auth/register | Register |
| POST | /api/auth/login | Login |
| GET | /api/expenses/ | List expenses |
| POST | /api/expenses/ | Add expense |
| PUT | /api/expenses/{id} | Update |
| DELETE | /api/expenses/{id} | Delete |
| GET | /api/expenses/summary/{month} | Monthly summary |
| GET | /api/expenses/ai-advice/{month} | AI advice |

## Run tests
```bash
cd backend && pytest app/tests/ -v
```
