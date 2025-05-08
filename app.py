import streamlit as st
from components.single_prediction import single_prediction_tab
from components.batch_prediction import batch_prediction_tab
from utils.style import load_css

def main():
    # Load CSS
    load_css()
    
    # App title
    st.title('🚚 Delivery Time Predictor')
    st.markdown("Predict delivery times using single input or batch processing")
    
    # Create tabs
    tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])
    
    with tab1:
        with st.container():
            single_prediction_tab()
    
    with tab2:
        with st.container():
            batch_prediction_tab()

if __name__ == "__main__":
    main()