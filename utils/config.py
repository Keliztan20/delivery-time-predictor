# Mapping dictionaries
VEHICLE_TYPE_MAPPING = {'Motorcycle': 1, 'Scooter': 2, 'Electric Scooter': 3, 'Others': 4}
VEHICLE_CONDITION_MAPPING = {'Excellent': 1, 'Good': 2, 'Fair': 3, 'Poor': 4}
WEATHER_OPTIONS = ['Sunny', 'Cloudy', 'Windy', 'Foggy', 'Sandstorms', 'Stormy']
TRAFFIC_OPTIONS = ['Low', 'Medium', 'High', 'Jammed']

# For batch processing
WEATHER_MAPPING = {
    'Sunny': 1,
    'Cloudy': 2,
    'Windy': 3,
    'Foggy': 4,
    'Sandstorms': 5,
    'Stormy': 6
}
TRAFFIC_MAPPING = {
    'Low': 1,
    'Medium': 2,
    'High': 3,
    'Jammed': 4
}

# Model path
MODEL_PATH = 'assets/Delivery_time_predictor.h5'