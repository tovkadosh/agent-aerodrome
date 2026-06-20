from fastapi import FastAPI
from pydantic import BaseModel
from agent import poser_question

app = FastAPI(title="Agent IA Aérodrome")

class Question(BaseModel):
    texte: str

@app.get("/")
def accueil():
    return {"message": "Agent IA Aérodrome - envoie une question à /demander"}

@app.post("/demander")
def demander(q: Question):
    reponse = poser_question(q.texte)
    return {"question": q.texte, "reponse": reponse}