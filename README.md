AI Tutor is an AI-powered placement preparation assistant that explains interview and placement-related topics in a simple, structured, and easy-to-understand format.

The system uses an agent-based workflow to generate clear explanations with headings, short paragraphs, bullet points, and an optional audio walkthrough. The application is built using a FastAPI backend and a Streamlit frontend.



## Overview

This project helps students prepare for placements and technical interviews by:

- Generating structured explanations  
- Keeping language simple and interview-focused  
- Controlling explanation length based on time duration  
- Providing audio-based revision  
- Ensuring only placement-related queries are accepted  

The architecture is modular and built using an agent-based workflow powered by LangGraph.



## Features

- Accepts placement-related questions from users  
- Validates questions using guardrails  
- Generates structured explanations in the format:
  - Concept heading  
  - Short paragraph explanation  
  - Bullet points  
- Controls explanation length (~150 words per minute)  
- Converts explanations into audio  
- Matches audio duration with selected time  
- Displays results in a clean Streamlit interface  

---

## Architecture – Agent-Based Workflow

The system uses LangGraph to orchestrate multiple agents in a structured flow.

### Guardrail Agent
- Validates whether the question is placement-related  
- Rejects irrelevant or unsafe queries  
- Prevents misuse of the system  

### Teacher Agent
- Uses Gemini (Free Tier) for content generation  
- Produces:
  - Concept heading  
  - Clear paragraph explanation  
  - Bullet points  
- Keeps explanations concise and interview-friendly  
- Limits content length based on selected duration (~150 words per minute)  

### Content Agent
- Converts generated explanation into audio using text-to-speech  
- Matches audio duration with the selected explanation time  
- Prevents excessively long or broken outputs  

---

## Project Structure


ai-tutor/
 │
 ├── app/
 │ ├── main.py # FastAPI backend entry point
 │ ├── graph.py # LangGraph workflow and agent logic
 │ └── knowledge_base.py # Placement topics and reference content
 │
 ├── ui/
 │ └── streamlit_app.py # Streamlit frontend interface
 │
 ├── .env # Gemini API key
 ├── requirements.txt
 └── README.md




## How to Run the Project

### 1. Create a Virtual Environment

bash
python -m venv venv


### Activate it:

*Windows*
bash
venv\Scripts\activate


*Mac/Linux*
bash
source venv/bin/activate


---

### 2. Install Dependencies

bash
pip install -r requirements.txt


---

### 3. Add Gemini API Key

Create a .env file in the root directory and add:


GEMINI_API_KEY=your_api_key_here


Make sure your backend loads environment variables correctly.

---

### 4. Start the Backend (FastAPI)

bash
uvicorn app.main:app --reload


Backend will run at:

http://127.0.0.1:8000


---

### 5. Start the Frontend (Streamlit)

In a new terminal:

bash
streamlit run ui/streamlit_app.py


The application will open automatically in your browser.



## Tech Stack

- Python 3.14  
- LangGraph – Agent orchestration  
- Gemini (Free Tier) – AI content generation  
- FastAPI – Backend API  
- Streamlit – Frontend UI  
- pyttsx3 – Text-to-speech audio generation  


## Design Goals

- Simple explanations for interview preparation  
- Structured and readable output  
- Controlled content length  
- Modular and scalable architecture  
- Clean separation between backend, agents, and UI  


## Future Improvements

- Add user authentication  
- Add session history tracking  
- Support multiple difficulty levels  
- Add support for additional AI models  
- Deploy using Docker and cloud hosting  

---

## License

This project is for educational purposes.
 
