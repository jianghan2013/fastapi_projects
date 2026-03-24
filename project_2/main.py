from fastapi import FastAPI
from .routers import cases

app = FastAPI()

app.include_router(cases.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
