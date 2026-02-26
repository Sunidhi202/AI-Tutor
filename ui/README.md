#  AI Tutor – Placement Preparation Assistant

This project is an **AI-based tutor** that explains **placement-related topics** in a **simple and structured way**.  
It uses an **agent-based workflow** to generate clear explanations with **headings, short paragraphs, and bullet points**, along with an **audio walkthrough**.

---

##  What This Project Does

- Takes a **placement-related question** from the user  
- Validates the question using **guardrails**
- Generates **easy-to-understand explanations**
- Presents content as:
  - Heading
  - Short paragraph
  - Bullet points
- Controls explanation length using **time duration**
- Generates **audio** for the explanation
- Displays everything in a clean **Streamlit UI**

---

## 🧠 Agent-Based Design (LangGraph)

The system uses **LangGraph** to manage the flow between agents:

### 🔹 Guardrail Agent
- Checks if the question is placement-related
- Rejects unrelated queries

### 🔹 Teacher Agent
- Uses **Gemini (free tier)** to generate explanations
- Produces:
  - Concept heading
  - Paragraph explanation
  - Bullet points
- Keeps language simple for interviews
- Limits content based on duration (≈150 words/min)

### 🔹 Media Agent
- Converts explanation into **audio**
- Ensures audio length matches selected duration
- Prevents long or broken audio output

---

## 🛠 Tech Stack

- **Python 3.14**
- **LangGraph** – agent orchestration
- **Gemini (free tier)** – content generation
- **FastAPI** – backend API
- **Streamlit** – frontend UI
- **pyttsx3** – text-to-speech audio

---

## 📁 Project Structure

ai-tutor/
│
├── app/
│ ├── main.py # FastAPI backend
│ ├── graph.py # LangGraph workflow
│ └── knowledge_base.py # Placement topics
│
├── ui/
│ └── streamlit_app.py # Streamlit UI
│
├── .env # Gemini API key
├── requirements.txt
└── README.md



### How to Run the Project

# 1️ Create virtual environment



## 2️ Install dependencies

### 3️ Add Gemini API key
Create a `.env` file:


#### 4️ Start backend
unicorn app.mainapp--reload

##### 5 Start frontend
using streamlit