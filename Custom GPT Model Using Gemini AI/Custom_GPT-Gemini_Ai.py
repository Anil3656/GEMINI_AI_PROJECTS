import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_API_KEY"] = "lsv2_pt_3d8bc461e1f146d79eef7efd26eec876_f8a7a6518de"

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Custom GPT using Gemini", layout="centered")

# -------------------------------
# GRADIENT CSS
# -------------------------------
gradient_css = """
<style>
body {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    height: 100vh;
    margin: 0;
    color: white;
}
.main-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 18px;
    margin-top: 20px;
    width: 70%;
    margin-left: auto;
    margin-right: auto;
}
.answer-box {
    background: white;
    padding: 15px;
    border-radius: 12px;
    margin-top: 15px;
    color: black;
    font-size: 18px;
}
.stButton>button {
    background: #ff7b00 !important;
    color: white !important;
    padding: 10px 18px;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    cursor: pointer;
}
.stButton>button:hover {
    background: #ff5500 !important;
}
</style>
"""
st.markdown(gradient_css, unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.markdown("<h1 style='text-align:center;'>⚡ Custom GPT using Gemini</h1>", unsafe_allow_html=True)

# -------------------------------
# LLM INIT
# -------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="AIzaSyDLgBerlKVS4jWuoO2uDUDgR2hg-VAyaQs"
)

prompt = PromptTemplate.from_template("Question: {question}")
chain = LLMChain(llm=llm, prompt=prompt)

# -------------------------------
# MAIN CARD
# -------------------------------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

user_input = st.text_input("💬 Ask anything:", placeholder="Type your query here...")

run_button = st.button("Generate")

# -------------------------------
# RUN LLM
# -------------------------------
if run_button:
    if user_input.strip() == "":
        st.warning("Please enter a valid question.")
    else:
        answer = chain.invoke({"question": user_input})
        st.markdown(f"<div class='answer-box'>{answer['text']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
footer_css = """
<style>
.footer {
    width: 100%;
    text-align: center;
    padding: 15px 0;
    margin-top: 40px;
    font-size: 18px;
    color: #ffffff;
    font-weight: 600;
    opacity: 0.9;
    animation: fadeIn 1.5s ease-in-out;
}

.footer span {
    background: linear-gradient(90deg, #ff8a00, #e52e71);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 20px;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
"""

st.markdown(footer_css, unsafe_allow_html=True)

st.markdown(
    "<div class='footer'>© 2025 Developed by <span>Aneel Kumar Muppana</span></div>",
    unsafe_allow_html=True
)