from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    message: str

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/orders")
async def process_input(request: UserInput):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a drive through assistant that can help with orders."},
            {"role": "user", "content": request.message}
        ]
    )
    return {"message": response.choices[0].message.content}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
