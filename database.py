# --- Imports ---
import sqlite3


# Create database and table
def initialize_database():
    connection = sqlite3.connect("donations.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Store changes and close database
    connection.commit()
    connection.close()


# Add donation amount to database
def add_donation(amount):
    connection = sqlite3.connect("donations.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO donations (amount) VALUES (?)", (amount,))
    connection.commit()
    connection.close()


# Get totalt donations from database
def get_total_donations():
    connection = sqlite3.connect("donations.db")
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(amount) FROM donations")
    total = cursor.fetchone()[0]
    connection.close()
    return total or 0


# Helper function to delete all content in db
def clear_donations():
    connection = sqlite3.connect("donations.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM donations")
    connection.commit()
    connection.close()
    