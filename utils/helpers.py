import streamlit as st
import pandas as pd
import lightgbm as lgb
from utils.config import (
    VEHICLE_CONDITION_MAPPING,
    VEHICLE_TYPE_MAPPING,
    MODEL_PATH
)

@st.cache_resource(ttl=3600)
def load_model():
    return lgb.Booster(model_file=MODEL_PATH)

def predict_single(model, input_features):
    input_df = pd.DataFrame([input_features])
    return model.predict(input_df)[0]

def predict_batch(model, df):
    # Calculate vehicle performance impact if needed
    if 'Vehicle_condition' in df.columns and 'Type_of_vehicle' in df.columns:
        df['Vehicle_performance_Impact'] = df.apply(
            lambda row: VEHICLE_CONDITION_MAPPING.get(str(row['Vehicle_condition']).title(), 4) * 
                       VEHICLE_TYPE_MAPPING.get(str(row['Type_of_vehicle']).title(), 4),
            axis=1
        )
    
    required_cols = [
        'Delivery_person_Age', 'Delivery_person_Ratings',
        'Weather_conditions', 'Road_traffic_density',
        'Vehicle_performance_Impact', 'multiple_deliveries',
        'Festival', 'Travel_Distance', 'pickup_time'
    ]
    
    # Ensure all required columns are present
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
    
    df['Predicted_Delivery_Time'] = model.predict(df[required_cols])
    return df

def safe_convert_column(series, mapping, default, col_name):
    """Convert text columns to numerical values safely"""
    try:
        if pd.api.types.is_numeric_dtype(series):
            return series.astype(int)
        return series.map(lambda x: mapping.get(str(x).title(), default))
    except Exception as e:
        st.warning(f"⚠️ Some values in {col_name} couldn't be converted, using defaults")
        return pd.Series([default] * len(series), [f"Conversion issue in {col_name}"])