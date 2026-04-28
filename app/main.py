from fastapi import FastAPI

from app.database import init_db
from app.routes.auth import router as auth_router
from app.routes.tickets import router as tickets_router

app = FastAPI(title="Ticket API", version="1.0.0")


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
def home():
    return {"status": "OK"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(auth_router)
app.include_router(tickets_router)
