from fastapi import FastAPI

from routes.tickets import router as tickets_router

app = FastAPI()


@app.get("/")
def home():
    return {"status": "OK"}


app.include_router(tickets_router)
