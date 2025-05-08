import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .main {
            max-width: 900px;
            padding: 2rem;
        }
        .stNumberInput, .stSelectbox, .stSlider {
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            width: 100%;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }
        .metric-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .header {
            color: #2c3e50;
            margin-bottom: 2rem;
        }
        .section {
            margin-bottom: 2.5rem;
        }
        .tab-container {
            border-radius: 10px;
            padding: 1.5rem;
            background: #ffffff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .file-uploader {
            border: 2px dashed #cccccc;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)