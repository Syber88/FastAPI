from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, annotated

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}