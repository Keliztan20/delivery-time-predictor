import streamlit as st
import pandas as pd
import lightgbm as lgb

# Load the saved model
@st.cache_resource
def load_model():
    return lgb.Booster(model_file='Methodology\Delivery_time_predictor.h5')

loaded_model = load_model()

# Mapping dictionaries
vehicle_type_mapping = {'Motorcycle': 1, 'Scooter': 2, 'Electric Scooter': 3, 'Others': 4}
vehicle_condition_mapping = {'Excellent': 1, 'Good': 2, 'Fair': 3, 'Poor': 4}
weather_options = ['Sunny', 'Cloudy', 'Windy','Foggy', 'Sandstorms', 'Stormy']
traffic_options = ['Low', 'Medium', 'High', 'Jammed']

# Custom CSS
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

# Prediction functions
def predict_single(input_features):
    input_df = pd.DataFrame([input_features])
    return loaded_model.predict(input_df)[0]

def predict_batch(df):
    if 'Vehicle_condition' in df.columns and 'Type_of_vehicle' in df.columns:
        df['Vehicle_performance_Impact'] = df.apply(
            lambda row: vehicle_condition_mapping.get(row['Vehicle_condition'], 4) * 
                       vehicle_type_mapping.get(row['Type_of_vehicle'], 4),
            axis=1
        )
    required_cols = ['Delivery_person_Age', 'Delivery_person_Ratings', 'Weather_conditions',
                   'Road_traffic_density', 'Vehicle_performance_Impact', 'multiple_deliveries',
                   'Festival', 'Travel_Distance', 'pickup_time']
    df['Predicted_Delivery_Time'] = loaded_model.predict(df[required_cols])
    return df

# Single Prediction Tab
def single_prediction_tab():
    with st.form("delivery_form"):
        st.subheader("Delivery Details")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("Delivery Person Age", 18, 60, 30)
        with col2:
            ratings = st.slider("Delivery Person Ratings", 1.0, 5.0, 4.2, step=0.1)
        
        col3, col4 = st.columns(2)
        with col3:
            weather = st.selectbox("Weather Conditions", weather_options)
        with col4:
            traffic = st.selectbox("Road Traffic Density", traffic_options)
        
        st.subheader("Vehicle Information")
        col5, col6 = st.columns(2)
        with col5:
            condition = st.selectbox("Vehicle Condition", list(vehicle_condition_mapping.keys()))
        with col6:
            vehicle_type = st.selectbox("Type of Vehicle", list(vehicle_type_mapping.keys()))
        
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
                'Weather_conditions': weather_options.index(weather) + 1,
                'Road_traffic_density': traffic_options.index(traffic) + 1,
                'Vehicle_performance_Impact': vehicle_condition_mapping[condition] * vehicle_type_mapping[vehicle_type],
                'multiple_deliveries': multi_deliveries,
                'Festival': 1 if festival else 0,
                'Travel_Distance': distance,
                'pickup_time': pickup_time
            }
            
            prediction = predict_single(input_features)
            
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

# Batch Prediction Tab
def batch_prediction_tab():
    st.subheader("📂 Batch Prediction from CSV")
    
    # Define all mappings
    WEATHER_MAPPING = {
        'Sunny': 1,
        'Cloudy': 2,
        'Windy': 3,
        'Fog': 4,
        'Sandstorms': 5,
        'Stormy': 6
    }
    TRAFFIC_MAPPING = {
        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Heavy': 4
    }
    VEHICLE_CONDITION_MAPPING = {
        'Excellent': 1,
        'Good': 2,
        'Fair': 3,
        'Poor': 4
    }
    VEHICLE_TYPE_MAPPING = {
        'Motorcycle': 1,
        'Scooter': 2,
        'Electric Scooter': 3,
        'Others': 4
    }

    # File uploader with modern styling
    st.markdown("""
    <div style="border: 2px dashed #ebfafa; border-radius: 10px; padding: 25px; text-align: center; margin: 20px 0; background-color: #262730;">
        <h4 style="color: #ebfafa;">Upload Your CSV File</h4>
        <p style="color: #7f8c8d;">Drag and drop your file here or click to browse</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(" ", type=["csv"], label_visibility="collapsed")

    # Guidance in expandable sections
    with st.expander("📋 CSV Requirements & Value Mappings", expanded=True):
        st.markdown("""
        **Required Columns:** Your CSV must include either:
        - Pre-calculated `Vehicle_performance_Impact` (numerical), OR
        - Both `Vehicle_condition` and `Type_of_vehicle` columns
        
        **Plus these mandatory fields:**
        """)
        
        req_cols = st.columns(2)
        with req_cols[0]:
            st.markdown("""
            - `Delivery_person_Age` (18-60)
            - `Delivery_person_Ratings` (1.0-5.0)
            - `multiple_deliveries` (1-4)
            - `Festival` (0 or 1)
            """)
        with req_cols[1]:
            st.markdown("""
            - `Travel_Distance` (km)
            - `pickup_time` (minutes)
            - `Weather_conditions` (text/number)
            - `Road_traffic_density` (text/number)
            """)
        
        st.markdown("---")
        st.markdown("**Text-to-Number Conversion Mappings:**")
        
        map_cols = st.columns(3)
        with map_cols[0]:
            st.markdown("""
            **Weather Conditions:**
            - Sunny → 1
            - Cloudy → 2
            - Windy → 3
            - Fog → 4
            - Sandstorms → 5
            - Stormy → 6
            """)
        with map_cols[1]:
            st.markdown("""
            **Vehicle Condition:**
            - Excellent → 1
            - Good → 2
            - Fair → 3
            - Poor → 4
            """)
        with map_cols[2]:
            st.markdown("""
            **Vehicle Type:**
            - Motorcycle → 1
            - Scooter → 2
            - Electric Scooter → 3
            - Others → 4
            """)

    # Sample data section
    with st.expander("💡 Download Sample CSV Template", expanded=False):
        sample_data = {
            'Delivery_person_Age': [25, 30, 35],
            'Delivery_person_Ratings': [4.5, 3.8, 4.2],
            'Weather_conditions': ['Sunny', 'Cloudy', 'Stormy'],
            'Road_traffic_density': ['Medium', 'High', 'Low'],
            'Vehicle_condition': ['Good', 'Fair', 'Excellent'],
            'Type_of_vehicle': ['Motorcycle', 'Scooter', 'Electric Scooter'],
            'multiple_deliveries': [1, 2, 0],
            'Festival': [0, 1, 0],
            'Travel_Distance': [5.5, 12.3, 8.1],
            'pickup_time': [30, 45, 15]
        }
        st.dataframe(pd.DataFrame(sample_data))
        
        csv = pd.DataFrame(sample_data).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Sample CSV",
            data=csv,
            file_name='delivery_data_template.csv',
            mime='text/csv',
            use_container_width=True,
            help="Download a template file with sample data"
        )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            REQUIRED_COLS = [
                'Delivery_person_Age', 'Delivery_person_Ratings',
                'Weather_conditions', 'Road_traffic_density',
                'multiple_deliveries', 'Festival',
                'Travel_Distance', 'pickup_time'
            ]
            
            # Check for vehicle performance columns
            has_performance_col = 'Vehicle_performance_Impact' in df.columns
            has_components = all(col in df.columns for col in ['Vehicle_condition', 'Type_of_vehicle'])
            
            if not (has_performance_col or has_components):
                st.error("❌ Missing vehicle data: Provide either Vehicle_performance_Impact OR both Vehicle_condition and Type_of_vehicle")
                st.stop()
            
            missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
            if missing_cols:
                st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                st.stop()
            
            # Conversion functions with validation
            def safe_convert(value, mapping, default, col_name):
                try:
                    if pd.api.types.is_numeric_dtype(value):
                        return value.astype(int)
                    return value.map(lambda x: mapping.get(str(x).title(), default))
                except Exception as e:
                    st.warning(f"⚠️ Some values in {col_name} couldn't be converted, using defaults")
                    return pd.Series([default] * len(value))
            
            # Convert text columns to numerical
            conversion_log = []
            
            if 'Weather_conditions' in df.columns:
                original = df['Weather_conditions'].head(5).tolist()
                df['Weather_conditions'] = safe_convert(df['Weather_conditions'], WEATHER_MAPPING, 1, 'Weather_conditions')
                conversion_log.append(("Weather", original, df['Weather_conditions'].head(5).tolist()))
            
            if 'Road_traffic_density' in df.columns:
                original = df['Road_traffic_density'].head(5).tolist()
                df['Road_traffic_density'] = safe_convert(df['Road_traffic_density'], TRAFFIC_MAPPING, 2, 'Traffic')
                conversion_log.append(("Traffic", original, df['Road_traffic_density'].head(5).tolist()))
            
            if not has_performance_col:
                if 'Vehicle_condition' in df.columns:
                    original = df['Vehicle_condition'].head(5).tolist()
                    df['Vehicle_condition'] = safe_convert(df['Vehicle_condition'], VEHICLE_CONDITION_MAPPING, 2, 'Condition')
                    conversion_log.append(("Condition", original, df['Vehicle_condition'].head(5).tolist()))
                
                if 'Type_of_vehicle' in df.columns:
                    original = df['Type_of_vehicle'].head(5).tolist()
                    df['Type_of_vehicle'] = safe_convert(df['Type_of_vehicle'], VEHICLE_TYPE_MAPPING, 1, 'Vehicle Type')
                    conversion_log.append(("Vehicle Type", original, df['Type_of_vehicle'].head(5).tolist()))
                
                df['Vehicle_performance_Impact'] = df['Vehicle_condition'] * df['Type_of_vehicle']
            
            # Show conversion log
            if conversion_log:
                with st.expander("🔍 Applied Conversions (First 5 Rows)", expanded=True):
                    for col_type, original, converted in conversion_log:
                        st.markdown(f"""
                        **{col_type} Column:**
                        - Original: `{original}`
                        - Converted to: `{converted}`
                        """)
            
            # Data preview
            with st.expander("👀 Preview Processed Data", expanded=True):
                st.dataframe(df.head(5))
            
            # Prediction section
            st.markdown("---")
            if st.button("🚀 Run Batch Predictions", type="primary", use_container_width=True):
                with st.spinner('Generating predictions...'):
                    try:
                        required_cols = [
                            'Delivery_person_Age', 'Delivery_person_Ratings',
                            'Weather_conditions', 'Road_traffic_density',
                            'Vehicle_performance_Impact', 'multiple_deliveries',
                            'Festival', 'Travel_Distance', 'pickup_time'
                        ]
                        
                        predictions = loaded_model.predict(df[required_cols])
                        result_df = df.copy()
                        result_df['Predicted_Delivery_Time'] = predictions
                        
                        st.success("✅ Successfully predicted {} deliveries!".format(len(result_df)))
                        
                        # Results display
                        with st.expander("📊 Prediction Results", expanded=True):
                            st.dataframe(result_df.head())
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Average Delivery Time", f"{result_df['Predicted_Delivery_Time'].mean():.1f} mins")
                            with col2:
                                st.metric("Longest Delivery", f"{result_df['Predicted_Delivery_Time'].max():.1f} mins")
                        
                        # Download options
                        st.markdown("---")
                        st.markdown("### 📥 Download Results")
                        
                        csv = result_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Full Results (CSV)",
                            data=csv,
                            file_name='delivery_predictions.csv',
                            mime='text/csv',
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Prediction failed: {str(e)}")
                        st.info("Please check your data columns and try again")
        
        except Exception as e:
            st.error(f"❌ File processing error: {str(e)}")
            st.info("""
            Common issues:
            1. File is not a valid CSV
            2. Missing required columns
            3. Invalid values in numeric fields
            """)

# Main App
def main():
    st.title('🚚 Delivery Time Predictor')
    st.markdown("Predict delivery times using single input or batch processing")
    
    tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])
    
    with tab1:
        with st.container():
            single_prediction_tab()
    
    with tab2:
        with st.container():
            batch_prediction_tab()
            
if __name__ == "__main__":
    main()