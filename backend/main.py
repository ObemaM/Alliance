from typing import Annotated
from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel

app = FastAPI()

class TTable(BaseModel):
    sas: int
    named: str | None = None

class TCountry (TTable):
    id: int
    name: str

class TTaskAdd (TCountry):
    gay: str

tasks = []

@app.post("/add")
async def post_add(
    task: Annotated[TTaskAdd, Depends()], # Двоеточие - подсказка типа, Depends() - зависимость
):
    tasks.append(task)
    return tasks

    
