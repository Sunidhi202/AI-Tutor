from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from app.knowledge_base import KNOWLEDGE_BASE
import uuid
import os
import pyttsx3
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Gemini Client (Free Tier)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Graph State

class TutorState(TypedDict):
    query: str
    duration: int
    allowed: bool
    sections: Optional[List[dict]]
    result: Optional[dict]


# Node A: Guardrail Agent

def guardrail_node(state: TutorState) -> TutorState:
    allowed = any(
        topic.lower() in state["query"].lower()
        for topic in KNOWLEDGE_BASE
    )

    if not allowed:
        return {
            **state,
            "allowed": False,
            "result": {
                "error": "Only placement-related topics are allowed."
            }
        }

    return {**state, "allowed": True}


# Node B: Teacher Agent 

def teacher_node(state: TutorState) -> TutorState:
    if not state["allowed"]:
        return state

    WORDS_PER_MIN = 150
    word_limit = state["duration"] * WORDS_PER_MIN

    prompt = f"""
You are a placement preparation tutor.

Explain the topic:
"{state['query']}"

Generate a STEP-BY-STEP walkthrough.

STRICT FORMAT (follow exactly):

Step 1: Title
Paragraph explanation (2–3 short lines).

- Bullet point
- Bullet point
- Bullet point

Step 2: Title
Paragraph explanation.

- Bullet point
- Bullet point

RULES:
- Each step explains ONE concept
- Simple language (placement interview level)
- No markdown
- No empty steps
- Paragraph + bullets both required
- Around {word_limit} words total
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    text = response.text.strip()

    sections = []
    current_title = None
    paragraph_lines = []
    bullet_lines = []

    for line in text.splitlines():
        line = line.strip()

        # New Step
        if line.lower().startswith("step"):
            if current_title and (paragraph_lines or bullet_lines):
                content = ""
                if paragraph_lines:
                    content += " ".join(paragraph_lines) + "\n\n"
                if bullet_lines:
                    content += "\n".join(bullet_lines)

                sections.append({
                    "title": current_title,
                    "content": content.strip()
                })

            parts = line.split(":", 1)
            current_title = parts[1].strip() if len(parts) == 2 else line
            paragraph_lines = []
            bullet_lines = []

        # Bullet
        elif line.startswith("-"):
            bullet = line.lstrip("-").strip()
            if bullet:
                bullet_lines.append(f"• {bullet}")

        # Paragraph line
        elif line:
            paragraph_lines.append(line)

    # Add last step
    if current_title and (paragraph_lines or bullet_lines):
        content = ""
        if paragraph_lines:
            content += " ".join(paragraph_lines) + "\n\n"
        if bullet_lines:
            content += "\n".join(bullet_lines)

        sections.append({
            "title": current_title,
            "content": content.strip()
        })

    return {**state, "sections": sections}

# Node C: Content

def content_node(state: TutorState) -> TutorState:
    sections = state.get("sections") or []

    if not sections:
        return {
            **state,
            "result": {
                "sections": [],
                "audio_file": None,
                "error": "No valid content generated"
            }
        }

    # Audio control
    WORDS_PER_MIN = 150
    max_words = state["duration"] * WORDS_PER_MIN

    audio_text = " ".join(
        section["content"] for section in sections
    )

    #  HARD LIMIT (prevents freeze + timing issues)
    audio_words = audio_text.split()[:max_words]
    audio_text = " ".join(audio_words)

    engine = pyttsx3.init()
    engine.setProperty("rate", 160)

    audio_file = f"audio_{uuid.uuid4()}.wav"
    engine.save_to_file(audio_text, audio_file)
    engine.runAndWait()

    return {
        **state,
        "result": {
            "sections": sections,
            "audio_file": audio_file
        }
    }


# Build LangGraph

graph = StateGraph(TutorState)

graph.add_node("guardrail", guardrail_node)
graph.add_node("teacher", teacher_node)
graph.add_node("content", content_node)

graph.set_entry_point("guardrail")
graph.add_edge("guardrail", "teacher")
graph.add_edge("teacher", "content")
graph.add_edge("content", END)

tutor_graph = graph.compile()