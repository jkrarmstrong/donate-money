# --- Imports ---
from flask import Flask, render_template, redirect, request, jsonify, url_for
from flask_cors import CORS
import stripe
from stripe_config import stripe


# ---  Initialize Flask application ---
app = Flask(__name__)
CORS(app) # lets frontend call backend with fetch/form
app.config['DEBUG'] = True


# --- Routes ---

# Route for home/index
@app.route('/')
def home():
    return render_template("home.html")


# Route for success after payment
@app.route("/success")
def success():
    return render_template("success.html")


# Route if payment gets's canceled
@app.route("/cancel")
def cancel():
    return render_template("cancel.html")


# Route to create a Stripe Checkout Session
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        
        # Get amount from frontend and convert to cents
        amount_in_usd = float(request.form["amount"])
        amount_in_cents = int(amount_in_usd * 100)

        # Create a new Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"], # Allow card payments
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Donation",
                    },
                    "unit_amount": amount_in_cents, # Amount in cents
                },
                "quantity": 1
            }],
            mode="payment", # One-time payment
            success_url=url_for("success", _external=True), # Redirect if success/no success
            cancel_url=url_for("cancel", _external=True),
        )
        # Redirect user to Stripe Checkout page
        return redirect(session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 400


# --- Flask main entry point ---
if __name__ == '__main__':
    app.run()