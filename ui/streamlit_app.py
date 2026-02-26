import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"
STATIC_URL = "http://127.0.0.1:8000/static"

st.set_page_config(
    page_title="AI Tutor🤖 ",
    page_icon="🤖",
    layout="centered"
)


st.markdown("""<style>
html, body { background-color: #0f1117; color: #e6e6eb; }
.stApp {
    background:
        radial-gradient(circle at top left, #1e293b 0%, transparent 45%),
        radial-gradient(circle at bottom right, #312e81 0%, transparent 45%),
        linear-gradient(180deg, #0f1117 0%, #020617 100%);
}
.card {
    background: linear-gradient(160deg, rgba(30,41,59,0.75), rgba(2,6,23,0.95));
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 20px;
}
.badge {
    background: rgba(99,102,241,0.15);
    padding: 6px 16px;
    border-radius: 999px;
    font-weight: 700;
}
</style>""", unsafe_allow_html=True)

# HEADER 
st.markdown("""
<div class="card">
  <div class="badge">AI POWERED TUTOR</div>
  <h1>🤖 AI Tutor</h1>
  <p>Ask Ques only related to your Placement !</p>
</div>
""", unsafe_allow_html=True)

# INPUT 
st.markdown('<div class="card">', unsafe_allow_html=True)

query = st.text_area(
    "Placement Query",
    placeholder="Typee...",
    height=90,
    label_visibility="collapsed"
)

duration = st.slider(
    "⏱️ Explanation Duration (minutes)",
    min_value=2,
    max_value=5,
    value=2
)

ask_btn = st.button("✨ Generate Explanation")
st.markdown('</div>', unsafe_allow_html=True)

# ---- OUTPUT ----
if ask_btn:
    if not query.strip():
        st.warning("⚠️ Please enter a valid placement-related question.")
    else:
        with st.spinner("🤖 Thinking like a tutor..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": query, "duration": duration},
                    timeout=120
                )

                if response.status_code != 200:
                    st.error("Backend error. Check FastAPI logs.")
                else:
                    data = response.json()

                    if "error" in data:
                        st.error(data["error"])
                    else:
                        for i, section in enumerate(data["sections"]):
                            if not section["title"] or not section["content"]:
                                continue  # 🔒 safety

                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.markdown(f'<div class="badge">STEP {i+1}</div>', unsafe_allow_html=True)
                            st.markdown(f"### {section['title']}")
                            st.write(section["content"])
                            st.markdown('</div>', unsafe_allow_html=True)

                        if data.get("audio_file"):
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.markdown('<div class="badge">AUDIO WALKTHROUGH</div>', unsafe_allow_html=True)
                            st.audio(f"{STATIC_URL}/{data['audio_file']}")
                            st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Connection error: {e}")