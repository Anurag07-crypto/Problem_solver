import streamlit as st
import sys
from pathlib import Path
import requests
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent))

# Page configuration
st.set_page_config(
    page_title="Student Assistant",
    page_icon="💬",
    layout="wide"
)

# Backend API configuration
BACKEND_URL = "http://127.0.0.1:8000/chat"

# Custom CSS
st.markdown("""
    <style>
        .chat-message {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
            animation: fadeIn 0.3s;
        }
        .user-message {
            background-color: #1f77e6;
            color: white;
            margin-left: 20%;
            text-align: right;
        }
        .bot-message {
            background-color: #f0f4ff;
            color: #1f77e6;
            margin-right: 20%;
            border-left: 4px solid #1f77e6;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .chat-header {
            text-align: center;
            color: #1f77e6;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="chat-header">💬 Student Assistant Chatbot</h1>', unsafe_allow_html=True)
st.markdown("Get instant answers to your questions using AI-powered RAG technology")
st.markdown('---')

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="chat-message user-message"><b>You:</b> {message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-message bot-message"><b>Assistant:</b> {message["content"]}</div>',
                unsafe_allow_html=True
            )

# Input section
st.markdown('---')

col1, col2 = st.columns([0.85, 0.15])

with col2:
    clear_chat = st.button("🗑️ Clear", use_container_width=True)
    if clear_chat:
        st.session_state.messages = []
        st.session_state.clear()
        st.rerun()

with col1:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Ask your question here...",
            placeholder="Type your question and press Enter",
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button("Send", use_container_width=True)

        if submit_button and user_input:
            try:
                # Add user message to history
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Show loading message
                with st.spinner("🔄 Processing your question..."):
                    response = requests.post(BACKEND_URL, json={"query": user_input}, timeout=30)
                    response.raise_for_status()
                    
                    data = response.json()
                    bot_response = data.get("response", "No response received")
                    
                    # Add bot response to history
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
                st.rerun()
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the backend server is running on http://127.0.0.1:8000")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ Backend error: {e.response.status_code}")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")