from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from utils.auth_utils import register_user, validate_login, requires_login
from utils.model_utils import predict_crop, predict_price
from utils.db_utils import get_marketplace_listings, add_marketplace_listing, get_user_listings

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if validate_login(email, password):
            session['user_email'] = email
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('signup.html')
        
        if register_user(name, email, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email already registered or registration failed.', 'danger')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Feature routes
@app.route('/crop-recommendation', methods=['GET', 'POST'])
@requires_login
def crop_recommendation():
    if request.method == 'POST':
        # Get form data
        nitrogen = float(request.form.get('nitrogen'))
        phosphorus = float(request.form.get('phosphorus'))
        potassium = float(request.form.get('potassium'))
        temperature = float(request.form.get('temperature'))
        humidity = float(request.form.get('humidity'))
        ph = float(request.form.get('ph'))
        rainfall = float(request.form.get('rainfall'))
        
        # Get prediction
        recommendation = predict_crop(nitrogen, phosphorus, potassium, 
                                      temperature, humidity, ph, rainfall)
        
        return render_template('crop_recommendation.html', recommendation=recommendation)
    
    return render_template('crop_recommendation.html')

@app.route('/price-prediction', methods=['GET', 'POST'])
@requires_login
def price_prediction():
    if request.method == 'POST':
        # Get form data
        crop_name = request.form.get('crop_name')
        region = request.form.get('region')
        season = request.form.get('season')
        
        # Get prediction
        predicted_price = predict_price(crop_name, region, season)
        
        return render_template('price_prediction.html', 
                               predicted_price=predicted_price,
                               crop_name=crop_name)
    
    return render_template('price_prediction.html')

@app.route('/marketplace')
def marketplace():
    listings = get_marketplace_listings()
    return render_template('marketplace.html', listings=listings)

@app.route('/marketplace/add', methods=['GET', 'POST'])
@requires_login
def add_listing():
    if request.method == 'POST':
        crop_name = request.form.get('crop_name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        description = request.form.get('description')
        
        user_email = session.get('user_email')
        
        if add_marketplace_listing(user_email, crop_name, quantity, price, description):
            flash('Listing added successfully!', 'success')
            return redirect(url_for('marketplace'))
        else:
            flash('Failed to add listing.', 'danger')
    
    return render_template('add_listing.html')

@app.route('/marketplace/my-listings')
@requires_login
def my_listings():
    user_email = session.get('user_email')
    listings = get_user_listings(user_email)
    return render_template('my_listings.html', listings=listings)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
