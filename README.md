# Ticket API

A FastAPI service for registering users, issuing JWT access tokens, and managing
support tickets owned by the authenticated user.

The API uses SQLAlchemy for persistence, Alembic for schema migrations, Pydantic
for request/response validation, and pytest for automated tests.

## Features

- User registration with unique email and username checks
- OAuth2 password login that returns a bearer JWT
- Authenticated `/auth/me` profile endpoint
- Per-user ticket CRUD endpoints
- Ticket status and priority enums
- SQLite development database by default
- Alembic migration support
- Docker and Docker Compose configuration
- Test suite covering health, auth, and ticket flows

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2
- Pydantic 2
- Alembic
- python-jose
- passlib/bcrypt
- pytest
- Ruff

## Project Structure

```text
.
+-- app/
|   +-- dependencies/     # FastAPI dependencies, including auth helpers
|   +-- models/           # SQLAlchemy models and enums
|   +-- routes/           # API route modules
|   +-- schemas/          # Pydantic request/response schemas
|   +-- config.py         # Environment-driven settings
|   +-- database.py       # SQLAlchemy engine/session setup
|   +-- main.py           # FastAPI app entry point
|   +-- security.py       # Password hashing helpers
+-- alembic/              # Database migrations
+-- tests/                # pytest suite
+-- Dockerfile
+-- docker-compose.yml
+-- env.example
+-- pyproject.toml
+-- requirements.txt
```

## Configuration

Settings are loaded from environment variables with the `TICKET_API_` prefix.
For local development, copy the example file:

```bash
cp env.example .env
```

Available settings:

| Variable | Default | Description |
| --- | --- | --- |
| `TICKET_API_DATABASE_URL` | `sqlite:///./ticket_api.db` | SQLAlchemy database URL |
| `TICKET_API_SECRET_KEY` | `your-secret-key-change-in-production` | Secret used to sign JWTs |
| `TICKET_API_ALGORITHM` | `HS256` | JWT signing algorithm |
| `TICKET_API_ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token lifetime |
| `TICKET_API_DEBUG` | `true` | Enables SQL echo and development behavior |
| `TICKET_API_APP_NAME` | `Ticket API` | Application name setting |
| `TICKET_API_VERSION` | `1.0.0` | Application version setting |

When `TICKET_API_DEBUG=false`, `TICKET_API_SECRET_KEY` must be set to a custom
value.

## Local Setup

Create and activate a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
cp env.example .env
```

Run migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

The service will be available at:

- API root: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Docker Setup

Build and start the API container:

```bash
docker compose up --build
```

The API is exposed at `http://127.0.0.1:8000`.

The compose file also defines a PostgreSQL service, but the API service is
configured to use SQLite by default. To use PostgreSQL, update
`TICKET_API_DATABASE_URL` to a PostgreSQL SQLAlchemy URL and ensure the required
database driver is installed.

## API Overview

### Health

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/` | No | Basic status response |
| `GET` | `/health` | No | Health check |

### Auth

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | No | Register a user |
| `POST` | `/auth/login` | No | Login and receive a bearer token |
| `GET` | `/auth/me` | Yes | Get the current user |

### Tickets

All ticket endpoints require a bearer token.

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/tickets/` | List tickets owned by the current user |
| `POST` | `/tickets/` | Create a ticket |
| `GET` | `/tickets/{ticket_id}` | Get a ticket by ID |
| `PUT` | `/tickets/{ticket_id}` | Update a ticket |
| `DELETE` | `/tickets/{ticket_id}` | Delete a ticket |

Ticket status values:

- `open`
- `in_progress`
- `resolved`
- `closed`

Ticket priority values:

- `low`
- `medium`
- `high`
- `urgent`

## Example Requests

Register a user:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "username": "alice",
    "password": "password123"
  }'
```

Login:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=password123"
```

Save the returned `access_token`, then call authenticated endpoints with:

```bash
Authorization: Bearer <access_token>
```

Create a ticket:

```bash
curl -X POST http://127.0.0.1:8000/tickets/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "Cannot log in",
    "description": "I cannot log in even though my password is correct.",
    "priority": "high"
  }'
```

Update a ticket:

```bash
curl -X PUT http://127.0.0.1:8000/tickets/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "status": "in_progress",
    "priority": "urgent"
  }'
```

List tickets:

```bash
curl http://127.0.0.1:8000/tickets/ \
  -H "Authorization: Bearer <access_token>"
```

## Database Migrations

Apply migrations:

```bash
alembic upgrade head
```

Create a new migration after changing models:

```bash
alembic revision --autogenerate -m "Describe change"
```

Roll back the latest migration:

```bash
alembic downgrade -1
```

## Testing

Run the test suite:

```bash
pytest
```

The tests use an in-memory SQLite database and override the application database
dependency, so they do not write to `ticket_api.db`.

## Code Quality

Run Ruff linting:

```bash
ruff check .
```

Format with Ruff:

```bash
ruff format .
```

## Notes

- `/auth/login` expects form data because it uses FastAPI's
  `OAuth2PasswordRequestForm`.
- Users can only access tickets where `owner_id` matches their authenticated
  user ID.
- `TicketUpdate` requires at least one field in the request body.
- The default SQLite database file is `ticket_api.db` in the project root.
