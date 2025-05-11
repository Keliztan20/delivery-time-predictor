import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .main {
            max-width: 900px;
            padding: 2rem;
            color:white;
        }
        .st-co, .st-ck {
               linear-gradient(to right, rgb(86, 146, 245) 0%, rgb(86, 146, 245) 28.5714%, rgb(86, 146, 245) 28.5714%, rgb(86, 146, 245) 100%); 
                }
        .stNumberInput, .stSelectbox, .stSlider {
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            background-color: #131720;
            color: white;
            border-radius: 8px; 
            border: 0.5px solid #3d4044;
            padding: 0.5rem 1rem;
            width: 100%;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #131730;
            transform: translateY(-2px);
            color:#ff4b43;
            border: 0.5px solid #ff4b43;
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
    </style>
    """, unsafe_allow_html=True)