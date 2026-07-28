from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserQuery(BaseModel):
    question: str

@app.post("/chat")
def chat(query: UserQuery):

    answer = my_agent.invoke(query.question)

    return {
        "answer": answer
    }