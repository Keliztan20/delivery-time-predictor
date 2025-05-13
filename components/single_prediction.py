import streamlit as st
from datetime import datetime, time
from utils.config import (
    WEATHER_OPTIONS,
    TRAFFIC_OPTIONS,
    VEHICLE_CONDITION_MAPPING,
    VEHICLE_TYPE_MAPPING
)
from utils.helpers import load_model, predict_single

def is_rush_hour(order_time):
    """Check if the order time falls within rush hour periods"""
    lunch_start = time(11, 0)
    lunch_end = time(14, 0)
    dinner_start = time(18, 0)
    dinner_end = time(21, 0)
    
    return (lunch_start <= order_time <= lunch_end) or (dinner_start <= order_time <= dinner_end)

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
            distance = st.number_input("Travel Distance (km)", 0.1, 100.0, 20.0, step=1.0)
            multi_deliveries = st.radio("Multiple Deliveries", options=[1, 0], format_func=lambda x: "Yes" if x else "No", horizontal=True)
        with col9:
            pickup_time = st.number_input("Pickup Time (minutes)", 0.1, 50.0, 5.0, step=1.0)
            festival = st.radio("Festival Period", options=[1, 0], format_func=lambda x: "Yes" if x else "No", horizontal=True)

        st.subheader("Order Details")
        col10, col11 = st.columns(2)
        with col10:
            order_date = st.date_input("Order Date", datetime.now())
        with col11:
            time_options = [time(h, m) for h in range(0, 24) for m in (0, 30)]
            order_time = st.selectbox(
                "Order Time",
                options=time_options,
                format_func=lambda t: t.strftime("%H:%M"),
                help="Select the time from the dropdown or Manual input"
            )
        
        submitted = st.form_submit_button("🚚 Predict Delivery Time", use_container_width=True)
    
    if submitted:
        with st.spinner('Calculating...'):
            # Calculate rush hour and day of week features
            rush_hour = 1 if is_rush_hour(order_time) else 0
            day_of_week = order_date.weekday()  # Monday=0, Sunday=6
            rush_day = rush_hour + day_of_week
            
            input_features = {
                'Delivery_person_Age': age,
                'Delivery_person_Ratings': ratings,
                'Weather_conditions': WEATHER_OPTIONS.index(weather) + 1,
                'Road_traffic_density': TRAFFIC_OPTIONS.index(traffic) + 1,
                'Vehicle_performance_Impact': VEHICLE_CONDITION_MAPPING[condition] * VEHICLE_TYPE_MAPPING[vehicle_type],
                'multiple_deliveries': multi_deliveries,
                'Festival': festival,
                'Travel_Distance': distance,
                'pickup_time': pickup_time,
                'rush_day': rush_day
            }
            
            prediction = predict_single(model, input_features)
            
            st.success("Prediction Complete!")
            with st.container():
                st.markdown(f"""
                <div class="metric-card" style="background-color: #F9F0F3; text-align: center;">
                    <h4 style="color: #2c3e50;">Estimated Delivery Time</h4>
                    <h1 style="color: #C31052; font-weight: bold;">{prediction:.2f} minutes</h1>
                    <p style="color: #7f8c8d;">Based on provided parameters & Trained Model</p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("Calculation Details `(Input Parameters)`"):
                col12, col13 = st.columns(2)
                with col12:                   
                    st.write(f"- Age: {age}")
                    st.write(f"- Weather: {weather}")
                    st.write(f"- Traffic: {traffic}")
                    st.write(f"- Distance: {distance} km")
                    st.write(f"- Pickup Time: {pickup_time} minutes")
                    st.write(f"- Order Date: {order_date.strftime('%Y-%m-%d')}")
                    st.write(f"- Order Time: {order_time.strftime('%H:%M')}")
                    st.write(f"- Festival: {'Yes' if festival else 'No'}")
                with col13:
                    st.write(f"- Ratings: {ratings} {'★' * int(round(ratings))}")
                    st.write(f"- Vehicle Type: {vehicle_type}")
                    st.write(f"- Vehicle Condition: {VEHICLE_CONDITION_MAPPING[condition]}")
                    st.write(f"- Multiple Deliveries: {'Yes' if multi_deliveries else 'No'}")                    
                    st.write(f"- Vehicle Performance Impact: {VEHICLE_CONDITION_MAPPING[condition] * VEHICLE_TYPE_MAPPING[vehicle_type]}")
                    st.write(f"- Day of Week: {day_of_week} ({order_date.strftime('%A')})")
                    st.write(f"- Rush Hour: {'Yes' if rush_hour else 'No'}")
                    st.write(f"- Rush Day Score: {rush_day}")