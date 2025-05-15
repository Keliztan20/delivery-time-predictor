import streamlit as st
import pandas as pd
from datetime import datetime, time
from utils.config import (
    WEATHER_MAPPING,
    TRAFFIC_MAPPING,
    VEHICLE_CONDITION_MAPPING,
    VEHICLE_TYPE_MAPPING,
    WEATHER_OPTIONS,
    TRAFFIC_OPTIONS
)
from utils.helpers import load_model

def is_rush_hour(time_str):
    """Check if the time string falls within rush hour periods"""
    try:
        order_time = datetime.strptime(time_str, '%H:%M').time()
        lunch_start = time(11, 0)
        lunch_end = time(14, 0)
        dinner_start = time(18, 0)
        dinner_end = time(21, 0)
        
        return (lunch_start <= order_time <= lunch_end) or (dinner_start <= order_time <= dinner_end)
    except:
        return False

def batch_prediction_tab():
    model = load_model()
    
    st.subheader("📂 Batch Prediction from CSV")

    # Guidance in expandable sections
    with st.expander("CSV Requirements & Value Mappings", expanded=False):
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
            - `multiple_deliveries` (0 or 1)
            - `Festival` (0 or 1)
            - `Order_Date`: Date in YYYY-MM-DD format
            """)
        with req_cols[1]:
            st.markdown("""
            - `Travel_Distance` (km)
            - `pickup_time` (minutes)
            - `Weather_conditions` (text/number)
            - `Road_traffic_density` (text/number)
            - `Time_Ordered`: HH:MM format (24-hour)
            """)
        st.markdown("**Note:** As `Order_Date` and `Time_Ordered` are missing, the current date and time will be used.")
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
            - Poor → 1
            - Fair → 2
            - Good → 3
            - Excellent → 4
            """)
        with map_cols[2]:
            st.markdown("""
            **Vehicle Type:**
            - Bicycle → 1
            - Electric Scooter → 2
            - Scooter → 3
            - Motorcycle → 4
            """)
    
    # Sample data section
    with st.expander("Show / Download Sample CSV Template", expanded=False):
        sample_data = {
            'Delivery_person_Age': [25, 30, 35],
            'Delivery_person_Ratings': [4.5, 3.8, 4.2],
            'Weather_conditions': ['Sunny', 'Cloudy', 'Stormy'],
            'Road_traffic_density': ['Medium', 'High', 'Low'],
            'Vehicle_condition': ['Good', 'Fair', 'Excellent'],
            'Type_of_vehicle': ['Motorcycle', 'Scooter', 'Electric Scooter'],
            'multiple_deliveries': [1, 0, 1],
            'Festival': [0, 1, 0],
            'Travel_Distance': [5.5, 12.3, 8.1],
            'pickup_time': [30, 45, 15],
            'Order_Date': ['2023-05-15', '2023-05-16', '2023-05-17'],
            'Time_Ordered': ['12:30', '19:15', '14:45']
        }
        st.dataframe(pd.DataFrame(sample_data))
        
        csv = pd.DataFrame(sample_data).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Sample CSV",
            data=csv,
            file_name='delivery_data_template.csv',
            mime='text/csv',
            use_container_width=True,
            help="Download a template file with sample data including new timing features"
        )
    
    uploaded_file = st.file_uploader(" ", type=["csv"], label_visibility="collapsed")

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
                st.error("Missing vehicle data: Provide either Vehicle_performance_Impact OR both Vehicle_condition and Type_of_vehicle")
                st.stop()
            
            missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                st.stop()
            
            # Add default timing columns if not provided
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M')
            
            if 'Order_Date' not in df.columns:
                df['Order_Date'] = current_date
                st.warning("Using current date for Order_Date (column not found)")
            
            if 'Time_Ordered' not in df.columns:
                df['Time_Ordered'] = current_time
                st.warning("Using current time for Time_Ordered (column not found)")
            
            # Conversion functions with validation
            def safe_convert(value, mapping, default, col_name):
                try:
                    if pd.api.types.is_numeric_dtype(value):
                        return value.astype(int)
                    return value.map(lambda x: mapping.get(str(x).replace('_', ' ').title(), default))
                except Exception as e:
                    st.warning(f"Some values in {col_name} couldn't be converted, using defaults")
                    return pd.Series([default] * len(value))
            
            # Convert text columns to numerical
            conversion_log = []
            
            if 'Weather_conditions' in df.columns:
                original = df['Weather_conditions'].head(10).tolist()
                df['Weather_conditions'] = safe_convert(df['Weather_conditions'], WEATHER_MAPPING, 1, 'Weather_conditions')
                conversion_log.append(("Weather", original, df['Weather_conditions'].head(10).tolist()))
            
            if 'Road_traffic_density' in df.columns:
                original = df['Road_traffic_density'].head(10).tolist()
                df['Road_traffic_density'] = safe_convert(df['Road_traffic_density'], TRAFFIC_MAPPING, 2, 'Traffic')
                conversion_log.append(("Traffic", original, df['Road_traffic_density'].head(10).tolist()))
            
            if not has_performance_col:
                if 'Vehicle_condition' in df.columns:
                    original = df['Vehicle_condition'].head(10).tolist()
                    df['Vehicle_condition'] = safe_convert(df['Vehicle_condition'], VEHICLE_CONDITION_MAPPING, 2, 'Vehicle Condition')
                    conversion_log.append(("Vehicle Condition", original, df['Vehicle_condition'].head(10).tolist()))
                
                if 'Type_of_vehicle' in df.columns:
                    original = df['Type_of_vehicle'].head(10).tolist()
                    df['Type_of_vehicle'] = safe_convert(df['Type_of_vehicle'].str.title(), VEHICLE_TYPE_MAPPING, 1, 'Vehicle Type')
                    conversion_log.append(("Vehicle Type", original, df['Type_of_vehicle'].head(10).tolist()))
                
                df['Vehicle_performance_Impact'] = df['Vehicle_condition'] * df['Type_of_vehicle']
            
            # Process timing features
            df['is_rush_hour'] = df['Time_Ordered'].apply(is_rush_hour).astype(int)
            df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d/%m/%Y')
            df['day_of_week'] = df['Order_Date'].dt.weekday  # Monday=0, Sunday=6
            df['rush_day'] = df['is_rush_hour'] + df['day_of_week']
            
            # Show conversion log
            if conversion_log:
                with st.expander("Applied Conversions (First 5 Rows)", expanded=True):
                    for col_type, original, converted in conversion_log:
                        st.markdown(f"""
                        **{col_type} Column:**
                        - Original: `{original}`
                        - Converted to: `{converted}`
                        """)
            
            # Data preview with new features
            with st.expander("Preview Processed Data", expanded=True):
                preview_cols = [
                    'Delivery_person_Age', 'Delivery_person_Ratings',
                    'Weather_conditions', 'Road_traffic_density',
                    'Vehicle_performance_Impact', 'is_rush_hour',
                    'day_of_week', 'rush_day', 'Festival',
                    'multiple_deliveries', 'Travel_Distance',
                ]
                st.dataframe(df[preview_cols].head(5))
            
            # Prediction section
            st.markdown("---")
            if st.button("🚀 Run Batch Predictions", use_container_width=True):
                with st.spinner('Generating predictions...'):
                    try:
                        required_cols = [
                            'Delivery_person_Age', 'Delivery_person_Ratings',
                            'Weather_conditions', 'Road_traffic_density',
                            'Vehicle_performance_Impact', 'multiple_deliveries',
                            'Festival', 'Travel_Distance', 'pickup_time', 'rush_day'
                        ]
                        
                        predictions = model.predict(df[required_cols])
                        result_df = df.copy()
                        result_df['Predicted_Delivery_Time'] = predictions
                        
                        st.success(f"Successfully predicted {len(result_df)} deliveries!")
                        
                        # Results display
                        with st.expander("Prediction Results", expanded=True):
                            st.dataframe(result_df.head())
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"""
                                    <div class="metric-card" style="background-color: #F9F0F3; text-align: center;">
                                        <h6 style="color: #2c3e50;">Average Delivery Time</h6>
                                        <h4 style="color: #C31052; font-weight: bold;">{result_df['Predicted_Delivery_Time'].mean():.1f} mins</h4>
                                        <p style="color: #7f8c8d; font-size: 12px;">Based on provided parameters & Trained Model</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"""
                                    <div class="metric-card" style="background-color: #F9F0F3; text-align: center;">
                                        <h6 style="color: #2c3e50;">Longest Delivery Time</h6>
                                        <h4 style="color: #C31052; font-weight: bold;">{result_df['Predicted_Delivery_Time'].max():.1f} mins</h4>
                                        <p style="color: #7f8c8d; font-size: 12px;">Based on provided parameters & Trained Model</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        # Download options
                        st.markdown("Download Results")
                        
                        csv = result_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Full Results (CSV)",
                            data=csv,
                            file_name='delivery_predictions.csv',
                            mime='text/csv',
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        st.error(f"Prediction failed: {str(e)}")
                        st.info("Please check your data columns and try again")
        
        except Exception as e:
            st.error(f"File processing error: {str(e)}")
            st.info("""
            Common issues:
            1. File is not a valid CSV
            2. Missing required columns
            3. Invalid values in numeric fields
            4. Incorrect date/time formats (should be YYYY-MM-DD and HH:MM)
            """)