# AgriTech Platform

A web application to help farmers with crop recommendations, price predictions, and marketplace access.

## Features

- **Crop Recommendation System**: Get personalized crop recommendations based on soil parameters and climate conditions.
- **Price Prediction**: Predict market prices for crops based on historical data, season, and region.
- **Marketplace**: Connect with buyers and sellers for agricultural products.

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/PrathamNiranjan/rendnew.git
   cd rendnew
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application locally:
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

### Deployment to Render

This application is configured for deployment on Render:

1. Create a new Web Service on Render
2. Link to your GitHub repository
3. Configure the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment Variables: Add `SECRET_KEY` with a secure random string

## Project Structure

```
├── app.py                # Main Flask application file
├── requirements.txt      # Dependencies
├── static/               # Static files
│   ├── css/              # CSS files
│   ├── js/               # JavaScript files
│   └── img/              # Images directory
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Home page
│   ├── login.html        # Login page
│   ├── signup.html       # Sign up page
│   ├── price_prediction.html
│   ├── crop_recommendation.html
│   └── marketplace.html
├── utils/                # Utility functions
│   ├── __init__.py
│   ├── auth_utils.py     # Authentication functions
│   ├── model_utils.py    # Model training and prediction
│   └── db_utils.py       # Database operations
├── data/                 # Data files
│   ├── price_data.csv
│   └── marketplace_data.csv
└── .gitignore            # Git ignore file
```

## License

This project is licensed under the MIT License
