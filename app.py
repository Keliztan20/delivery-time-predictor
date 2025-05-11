import subprocess
import streamlit as st
from components.single_prediction import single_prediction_tab
from components.batch_prediction import batch_prediction_tab
from utils.style import load_css

def main():
    # Load CSS
    load_css()
    
    # App title
    st.markdown(
        """
        <h1 style="display: flex; align-items: center;">
            <span>🚚༄ </span>
            <span style="margin-left: 20px;">Delivery Time Predictor</span>
        </h1>
        <style>
        @keyframes move {
            0% { transform: translateX(0); }
            50% { transform: translateX(10px); }
            100% { transform: translateX(0); }
        }
        h1 span:first-child {
            display: inline-block;
            animation: move 1.5s infinite;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("Predict delivery times using single delivery input or batch delivery processing")
    
    # Create tabs with plain text labels
    tab1, tab2 = st.tabs(
        [
            "Single Prediction",
            "Batch Prediction"
        ]
    )
    
    # Add custom CSS for tabs
    st.markdown(
        """
        <style>
        div[data-testid="stTabs"] button {
            font-size: 16px;
            font-weight: bold;
            color: black;
            border-radius: 6px;
            padding: 8px 16px;
            margin-right: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        }
        div[data-testid="stTabs"] button:hover {
            background-color: #F9F0F3;
            color: #C31052;
            transform: translateY(3px);
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            background-color: #F9F0F3;
            color: #C31052;
            transform: translateY(0);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with tab1:
        with st.container():
            single_prediction_tab()
    
    with tab2:
        with st.container():
            batch_prediction_tab()

if __name__ == "__main__":
    # Run LightGBM script only once
    # if "lightgbm_initialized" not in st.session_state:
    #     subprocess.run(["python", "assets/LightGBM.py"])
    #     st.session_state["lightgbm_initialized"] = True
    main()