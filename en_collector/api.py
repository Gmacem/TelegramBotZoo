from loguru import logger
from fastapi import FastAPI
from pydantic import BaseModel

app: FastAPI = FastAPI()


@app.get("/api/encollector/telegram")
async def root():
    pass