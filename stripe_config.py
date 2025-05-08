# --- Imports ---
import stripe
import os
from dotenv import load_dotenv

# Load all enviroment variables
load_dotenv()


# --- API Keys ---
# Secret key (test)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# Publishable key (test)
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")


