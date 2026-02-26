from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.graph import tutor_graph

app = FastAPI(title="AI Tutor using LangGraph")

# Serve generated audio files
app.mount("/static", StaticFiles(directory="."), name="static")


# Request Schema

class TutorRequest(BaseModel):
    query: str
    duration: int = 2


# API Endpoint

@app.post("/ask")
async def ask_tutor(req: TutorRequest):
    state = {
        "query": req.query,
        "duration": req.duration,
        "allowed": True,
        "sections": None,
        "result": None
    }

    final_state = tutor_graph.invoke(state)
    return final_state["result"]