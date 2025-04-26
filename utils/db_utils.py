import os
import json
import pandas as pd
from datetime import datetime

# In a real application, use a proper database
# This is simplified for demonstration purposes
MARKETPLACE_DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'marketplace_data.json')

def _load_marketplace_data():
    if not os.path.exists(MARKETPLACE_DB_FILE):
        os.makedirs(os.path.dirname(MARKETPLACE_DB_FILE), exist_ok=True)
        return []
    
    try:
        with open(MARKETPLACE_DB_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _save_marketplace_data(data):
    os.makedirs(os.path.dirname(MARKETPLACE_DB_FILE), exist_ok=True)
    with open(MARKETPLACE_DB_FILE, 'w') as file:
        json.dump(data, file)

def _initialize_data():
    """Initialize sample data if it doesn't exist"""
    if not os.path.exists(MARKETPLACE_DB_FILE):
        # Create sample marketplace data
        sample_data = [
            {
                "id": 1,
                "user_email": "farmer@example.com",
                "crop_name": "Rice",
                "quantity": "500 kg",
                "price": 2500,
                "description": "Organic basmati rice from Northern region",
                "date_posted": "2025-04-20"
            },
            {
                "id": 2,
                "user_email": "grower@example.com",
                "crop_name": "Wheat",
                "quantity": "1000 kg",
                "price": 3000,
                "description": "Premium quality wheat, ready for delivery",
                "date_posted": "2025-04-22"
            },
            {
                "id": 3,
                "user_email": "farmer@example.com",
                "crop_name": "Potatoes",
                "quantity": "200 kg",
                "price": 1200,
                "description": "Fresh potatoes harvested this week",
                "date_posted": "2025-04-24"
            }
        ]
        _save_marketplace_data(sample_data)

_initialize_data()

def get_marketplace_listings():
    """Get all marketplace listings"""
    return _load_marketplace_data()

def add_marketplace_listing(user_email, crop_name, quantity, price, description):
    """Add a new marketplace listing"""
    try:
        listings = _load_marketplace_data()
        
        # Generate a new ID (simple approach)
        new_id = 1
        if listings:
            new_id = max(item["id"] for item in listings) + 1
        
        # Create new listing
        new_listing = {
            "id": new_id,
            "user_email": user_email,
            "crop_name": crop_name,
            "quantity": quantity,
            "price": float(price),
            "description": description,
            "date_posted": datetime.now().strftime("%Y-%m-%d")
        }
        
        listings.append(new_listing)
        _save_marketplace_data(listings)
        return True
    except Exception as e:
        print(f"Error adding marketplace listing: {e}")
        return False

def get_user_listings(user_email):
    """Get listings for a specific user"""
    listings = _load_marketplace_data()
    return [item for item in listings if item["user_email"] == user_email]
