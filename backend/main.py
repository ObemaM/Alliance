from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TTable(BaseModel):
    sas: int
    named: str | None = None

class TCountry (TTable):
    id: int
    name: str

@app.get("/home")
def get_home():
    Check = Table(sas = 1, named = "Лох")
    return f"Hello world {Check}"

@app.get("/countries")
def get_countries():
    return