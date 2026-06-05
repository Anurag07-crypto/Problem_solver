import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st 

# Page configuration
st.set_page_config(
    page_title="Problem Solver",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #1f77e6;
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .feature-card {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f4ff;
            border-left: 4px solid #1f77e6;
            margin-bottom: 15px;
        }
        .feature-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #1f77e6;
            margin-bottom: 8px;
        }
        .feature-desc {
            color: #555;
            font-size: 0.95em;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎓 Problem Solver</div>', unsafe_allow_html=True)
st.markdown('---')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📚 Student Assistant</div>
        <div class="feature-desc">Get AI-powered answers to your questions using RAG technology with instant responses.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🎥 YouTube Finder</div>
        <div class="feature-desc">Find the best YouTube videos based on engagement rates and relevance to your query.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">⚡ Fast & Smart</div>
        <div class="feature-desc">Powered by advanced AI and machine learning for accurate and quick results.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('---')
st.markdown("""
<div style='text-align: center; margin-top: 40px;'>
    <h3>Get Started</h3>
    <p>Use the sidebar to navigate to different features or select from the pages menu.</p>
</div>
""", unsafe_allow_html=True)