import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .main {
            max-width: 900px;
            padding: 2rem;
            color:white;
        }
        .stNumberInput, .stSelectbox, .stSlider {
            margin-bottom: 1.5rem !important;
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
            box-shadow: 0 2px 4px rgba(0,0,0,0.0.5);
        }
        .stSelectbox:hover .stSelectbox-value, .stSelectbox:focus .stSelectbox-value {
            color: #E284A7;
            background-color: #E284A7;
        }
        .stSelectbox .stSelectbox-arrow {
            transition: color 0.3s ease;
        }
        .stSelectbox:hover .stSelectbox-arrow, .stSelectbox:focus .stSelectbox-arrow {
            color: #E284A7;
            background-color: #E284A7;
        }
    </style>
    """, unsafe_allow_html=True)