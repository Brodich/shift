from fastapi import FastAPI
from database import *

app = FastAPI()

@app.get("/")
async def home():
    return {"data": "Hello World"}
    
@app.get("/login")
async def login():
    


