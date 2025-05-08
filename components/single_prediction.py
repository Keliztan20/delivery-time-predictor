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
        col7, col8, col9 = st.columns(3)
        with col7:
            multi_deliveries = st.slider("Multiple Deliveries", 1, 5, 1)
        with col8:
            distance = st.number_input("Travel Distance (km)", 0.1, 100.0, 5.0, step=0.1)
        with col9:
            pickup_time = st.number_input("Pickup Time (minutes)", 0.1, 100.0, 20.0, step=1.0)
        
        festival = st.checkbox("During Festival Period", False)
        
        submitted = st.form_submit_button("🚚 Predict Delivery Time", use_container_width=True)
    
    if submitted:
        with st.spinner('Calculating...'):
            input_features = {
                'Delivery_person_Age': age,
                'Delivery_person_Ratings': ratings,
                'Weather_conditions': WEATHER_OPTIONS.index(weather) + 1,
                'Road_traffic_density': TRAFFIC_OPTIONS.index(traffic) + 1,
                'Vehicle_performance_Impact': VEHICLE_CONDITION_MAPPING[condition] * VEHICLE_TYPE_MAPPING[vehicle_type],
                'multiple_deliveries': multi_deliveries,
                'Festival': 1 if festival else 0,
                'Travel_Distance': distance,
                'pickup_time': pickup_time
            }
            
            prediction = predict_single(model, input_features)
            
            st.success("Prediction Complete!")
            with st.container():
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #2c3e50; margin-top: 0;">Estimated Delivery Time</h4>
                    <h1 style="color: #4CAF50; text-align: center;">{prediction:.2f} minutes</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("Calculation Details"):
                col10, col11 = st.columns(2)
                with col10:
                    st.markdown("**Input Parameters**")
                    st.write(f"- Age: {age}")
                    st.write(f"- Weather: {weather}")
                    st.write(f"- Traffic: {traffic}")
                    st.write(f"- Distance: {distance} km")
                with col11:
                    st.write(f"- Ratings: {ratings} ★")
                    st.write(f"- Type: {vehicle_type}")
                    st.write(f"- Condition: {condition}")
                    st.write(f"- Multiple Deliveries: {multi_deliveries}")
                    st.write(f"- Festival: {'Yes' if festival else 'No'}")