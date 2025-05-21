# --- Imports ---
from flask import Flask, render_template, redirect, request, jsonify, url_for
from flask_cors import CORS
import stripe
import click
from database import initialize_database, add_donation, clear_donations, get_total_donations
from stripe_config import stripe
from datetime import datetime
import os


# --- Initialize database ---
initialize_database()


# ---  Initialize Flask application ---
app = Flask(__name__)
CORS(app) # lets frontend call backend with fetch/form


# --- Initialize database ---
@app.cli.command("init-db")
def init_db_command():
    """Initialize database."""
    initialize_database()
    click.echo("Database initialized.")


# --- Clear all database content ----
@app.cli.command("clear-db")
def clear_db_command():
    """Clear donations db content."""
    clear_donations()
    click.echo("All donations are cleared.")


# --- Routes ---

# Route for home/index
@app.route("/")
def home():
    total_donations = get_total_donations()
    return render_template("home.html", total_donations=total_donations, now=datetime.now())


# Route for success after payment
@app.route("/success")
def success():
    session_id = request.args.get("session_id")
    if not session_id:
        return "Ingen session ID", 400

    session = stripe.checkout.Session.retrieve(session_id)
    amount_total = session.get("amount_total", 0)
    amount_in_usd = int(amount_total / 100)

    add_donation(amount_in_usd)
    
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
            success_url=url_for("success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}", # Redirect if success/no success
            cancel_url=url_for("cancel", _external=True),
        )
        # Redirect user to Stripe Checkout page
        return redirect(session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 400



# --- Flask main entry point ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)