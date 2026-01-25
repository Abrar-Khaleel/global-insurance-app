import sqlite3
from db_setup import create_connection

# --- CUSTOMER MANAGEMENT ---

def add_customer(first_name, last_name, email, phone, address):
    """Inserts a new customer into the database."""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO customers (first_name, last_name, email, phone, address)
            VALUES (?, ?, ?, ?, ?)
        """, (first_name, last_name, email, phone, address))
        conn.commit()
        return True, "Customer added successfully."
    except sqlite3.IntegrityError:
        return False, "Error: Email already exists."
    except Exception as e:
        return False, f"Database Error: {e}"
    finally:
        conn.close()

def get_all_customers():
    """Retrieves all customers for the list view."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, first_name, last_name, email, phone FROM customers")
    results = cursor.fetchall()
    conn.close()
    return results

def search_customers(last_name):
    """Search functionality for finding specific customers."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_id, first_name, last_name, email, phone 
        FROM customers 
        WHERE last_name LIKE ?
    """, ('%' + last_name + '%',))
    results = cursor.fetchall()
    conn.close()
    return results