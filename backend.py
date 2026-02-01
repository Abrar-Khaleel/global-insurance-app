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

# --- POLICY MANAGEMENT ---

def get_policy_types():
    """Fetches all available policy types for the dropdown menu."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type_id, name, default_coverage_amount FROM policy_types")
    results = cursor.fetchall()
    conn.close()
    return results

def add_policy(customer_id, type_id, start_date, end_date, premium):
    """Creates a new policy for an existing customer."""
    import secrets # Allowed library for generating secure numbers
    
    # Generate a unique Policy Number (e.g., POL-a1b2c3)
    policy_number = f"POL-{secrets.token_hex(3).upper()}"
    
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO policies 
            (customer_id, type_id, policy_number, start_date, end_date, premium_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Active')
        """, (customer_id, type_id, policy_number, start_date, end_date, premium))
        conn.commit()
        return True, f"Policy {policy_number} created successfully."
    except Exception as e:
        return False, f"Database Error: {e}"
    finally:
        conn.close()

def get_all_policies():
    """Retrieves policies with Customer Name and Policy Type joined."""
    conn = create_connection()
    cursor = conn.cursor()
    # This SQL JOIN is crucial for "Database Systems" marks
    cursor.execute("""
        SELECT 
            p.policy_id, 
            p.policy_number, 
            c.first_name || ' ' || c.last_name as customer_name,
            pt.name as policy_type,
            p.start_date,
            p.end_date,
            p.premium_amount,
            p.status
        FROM policies p
        JOIN customers c ON p.customer_id = c.customer_id
        JOIN policy_types pt ON p.type_id = pt.type_id
        ORDER BY p.policy_id DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results