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

# --- CLAIMS MANAGEMENT ---

def get_active_policies():
    """Fetches active policies to populate the 'File Claim' dropdown."""
    conn = create_connection()
    cursor = conn.cursor()
    # We fetch ID and Policy Number for the dropdown
    cursor.execute("""
        SELECT p.policy_id, p.policy_number, c.first_name, c.last_name 
        FROM policies p
        JOIN customers c ON p.customer_id = c.customer_id
        WHERE p.status = 'Active'
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def file_claim(policy_id, date_filed, claim_amount, incident_date, location, description):
    """
    ATOMIC TRANSACTION: Creates a Claim AND the associated Incident report.
    If one fails, both are rolled back.
    """
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Insert the Claim
        cursor.execute("""
            INSERT INTO claims (policy_id, date_filed, claim_amount, status)
            VALUES (?, ?, ?, 'Pending')
        """, (policy_id, date_filed, claim_amount))
        
        # Capture the ID of the claim we just created
        new_claim_id = cursor.lastrowid
        
        # 2. Insert the Incident (linked to the new claim_id)
        cursor.execute("""
            INSERT INTO incidents (claim_id, incident_date, location, description)
            VALUES (?, ?, ?, ?)
        """, (new_claim_id, incident_date, location, description))
        
        conn.commit()
        return True, "Claim and Incident Report filed successfully."
        
    except Exception as e:
        conn.rollback() # Undo changes if error occurs
        return False, f"Transaction Failed: {e}"
    finally:
        conn.close()

def get_all_claims():
    """Fetches claims joined with Policy and Customer info for the dashboard."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            cl.claim_id,
            p.policy_number,
            c.first_name || ' ' || c.last_name,
            cl.date_filed,
            cl.claim_amount,
            cl.status
        FROM claims cl
        JOIN policies p ON cl.policy_id = p.policy_id
        JOIN customers c ON p.customer_id = c.customer_id
        ORDER BY cl.date_filed DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def process_claim(claim_id, status, approved_amount=0.0):
    """
    Updates the status of a pending claim.
    If approved, automatically generates a payout record in the payments table.
    """
    from datetime import date
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Look up the policy_id associated with this claim
        cursor.execute("SELECT policy_id FROM claims WHERE claim_id = ?", (claim_id,))
        result = cursor.fetchone()
        if not result:
            return False, "Claim not found."
        policy_id = result[0]

        # 2. Update the Claim record
        cursor.execute("""
            UPDATE claims
            SET status = ?, approved_amount = ?
            WHERE claim_id = ?
        """, (status, approved_amount, claim_id))

        # 3. If Approved, log the financial transaction
        if status == 'Approved' and float(approved_amount) > 0:
            today = date.today().strftime("%Y-%m-%d")
            cursor.execute("""
                INSERT INTO payments (policy_id, amount, payment_date, payment_type)
                VALUES (?, ?, ?, 'Claim Payout')
            """, (policy_id, float(approved_amount), today))

        conn.commit()
        return True, f"Claim #{claim_id} has been {status}."
        
    except Exception as e:
        conn.rollback() # Cancel everything if an error occurs
        return False, f"Database Error: {e}"
    finally:
        conn.close()