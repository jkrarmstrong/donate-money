# --- Imports ---
from flask import Flask, render_template, redirect, request
from flask_cors import CORS
import stripe
from stripe_config import stripe


# ---  Initialize Flask application
app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True


# --- Routes ---
@app.route('/')
def home():
    return render_template('home.html')






# --- Flask main entry point ---
if __name__ == '__main__':
    app.run()