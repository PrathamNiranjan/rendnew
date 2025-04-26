import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# In a real application, you would have properly trained models
# This is simplified for demonstration purposes

# Paths to data files
PRICE_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'price_data.csv')

def _initialize_data():
    """Initialize sample data if it doesn't exist"""
    if not os.path.exists(PRICE_DATA_PATH):
        os.makedirs(os.path.dirname(PRICE_DATA_PATH), exist_ok=True)
        
        # Create sample price data
        crops = ['Rice', 'Wheat', 'Maize', 'Potatoes', 'Tomatoes']
        regions = ['North', 'South', 'East', 'West', 'Central']
        seasons = ['Summer', 'Winter', 'Monsoon']
        
        data = []
        for crop in crops:
            for region in regions:
                for season in seasons:
                    # Generate some realistic price data
                    base_price = np.random.randint(1000, 5000)
                    price = base_price + (100 if season == 'Summer' else 0) + (200 if region == 'North' else 0)
                    data.append([crop, region, season, price])
        
        price_df = pd.DataFrame(data, columns=['crop_name', 'region', 'season', 'price'])
        price_df.to_csv(PRICE_DATA_PATH, index=False)

_initialize_data()

def predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    """
    Predict the best crop based on soil parameters and climate conditions
    
    In a real application, this would use a properly trained model.
    This is a simplified example to demonstrate the concept.
    """
    # This is a simplified prediction logic
    if ph < 5.5:
        if rainfall > 200:
            return "Rice"
        else:
            return "Potatoes"
    elif nitrogen > 120:
        if phosphorus > 100:
            return "Sugarcane"
        else:
            return "Cotton"
    elif temperature > 30:
        if humidity > 80:
            return "Jute"
        else:
            return "Wheat"
    else:
        return "Maize"

def predict_price(crop_name, region, season):
    """
    Predict crop prices based on historical data
    
    In a real application, this would use a properly trained model.
    This is a simplified example to demonstrate the concept.
    """
    try:
        # Load the price data
        price_data = pd.read_csv(PRICE_DATA_PATH)
        
        # Simple filtering to get the average price
        filtered_data = price_data[
            (price_data['crop_name'] == crop_name) & 
            (price_data['region'] == region) & 
            (price_data['season'] == season)
        ]
        
        if filtered_data.empty:
            # If no exact match, get average for just the crop
            return float(price_data[price_data['crop_name'] == crop_name]['price'].mean())
        
        return float(filtered_data['price'].mean())
    except Exception as e:
        print(f"Error predicting price: {e}")
        return 0
