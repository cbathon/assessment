from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": api_key}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
