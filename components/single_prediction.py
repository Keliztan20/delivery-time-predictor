import streamlit as st
from utils.config import (
    WEATHER_OPTIONS,
    TRAFFIC_OPTIONS,
    VEHICLE_CONDITION_MAPPING,
    VEHICLE_TYPE_MAPPING
)
from utils.helpers import load_model, predict_single

def single_prediction_tab():
    model = load_model()
    
    with st.form("delivery_form"):
        st.subheader("Delivery Details")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("Delivery Person Age", 18, 60, 30)
        with col2:
            ratings = st.slider("Delivery Person Ratings", 1.0, 5.0, 4.2, step=0.1)
        
        col3, col4 = st.columns(2)
        with col3:
            weather = st.selectbox("Weather Conditions", WEATHER_OPTIONS)
        with col4:
            traffic = st.selectbox("Road Traffic Density", TRAFFIC_OPTIONS)
        
        st.subheader("Vehicle Information")
        col5, col6 = st.columns(2)
        with col5:
            condition = st.selectbox("Vehicle Condition", list(VEHICLE_CONDITION_MAPPING.keys()))
        with col6:
            vehicle_type = st.selectbox("Type of Vehicle", list(VEHICLE_TYPE_MAPPING.keys()))
        
        st.subheader("Delivery Parameters")
        col8, col9 = st.columns(2)
        with col8:
            distance = st.number_input("Travel Distance (km)", 0.1, 100.0, 50.0, step=1.0)
            multi_deliveries = st.radio("Multiple Deliveries", options=[1, 0], format_func=lambda x: "Yes" if x else "No", horizontal=True)
        with col9:
            pickup_time = st.number_input("Pickup Time (minutes)", 0.1, 100.0, 20.0, step=1.0)
            festival = st.radio("Festival Period", options=[1, 0], format_func=lambda x: "Yes" if x else "No", horizontal=True)
        
        submitted = st.form_submit_button("🚚 Predict Delivery Time", use_container_width=True)
    
    if submitted:
        # Validate pickup_time vs distance
        if pickup_time >= distance: 
            st.warning("Pickup time cannot be greater or equal than travel distance!! Please verify your inputs.")
        else:
            with st.spinner('Calculating...'):
                input_features = {
                    'Delivery_person_Age': age,
                    'Delivery_person_Ratings': ratings,
                    'Weather_conditions': WEATHER_OPTIONS.index(weather) + 1,
                    'Road_traffic_density': TRAFFIC_OPTIONS.index(traffic) + 1,
                    'Vehicle_performance_Impact': VEHICLE_CONDITION_MAPPING[condition] * VEHICLE_TYPE_MAPPING[vehicle_type],
                    'multiple_deliveries': 1 if multi_deliveries else 0,
                    'Festival': 1 if festival else 0,
                    'Travel_Distance': distance,
                    'pickup_time': pickup_time
                }
                
                prediction = predict_single(model, input_features)
                
                st.success("Prediction Complete!")
                with st.container():
                    st.markdown(f"""
                    <div class="metric-card" style="background-color: #F9F0F3; text-align: center;">
                        <h4 style="color: #2c3e50;">Estimated Delivery Time</h4>
                        <h1 style="color: #C31052;">{prediction:.2f} minutes</h1>
                        <p style="color: #7f8c8d; ">Based on provided parameters & Trained Model</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.expander("Calculation Details"):
                    col10, col11 = st.columns(2)
                    with col10:
                        st.write("##### `Input Parameters`")
                        st.write(f"- Age: {age}")
                        st.write(f"- Weather: {weather}")
                        st.write(f"- Traffic: {traffic}")
                        st.write(f"- Distance: {distance} km")
                        st.write(f"- Pickup Time: {pickup_time} minutes")
                    with col11:
                        st.write(f"- Ratings: {ratings} {'★' * int(round(ratings))}")
                        st.write(f"- Vehicle Type: {vehicle_type}")
                        st.write(f"- Vehicle Condition: {condition}")
                        st.write(f"- Multiple Deliveries: {'Yes' if multi_deliveries else 'No'}")
                        st.write(f"- Festival: {'Yes' if festival else 'No'}")
                        st.write(f"- Vehicle Performance Impact: {VEHICLE_CONDITION_MAPPING[condition] * VEHICLE_TYPE_MAPPING[vehicle_type]}")