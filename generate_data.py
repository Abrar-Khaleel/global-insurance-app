import random
import secrets
from datetime import timedelta
from faker import Faker
from db_setup import create_connection

# Initialize Faker to generate realistic mock data
fake = Faker()

# Configuration: How much data do we want?
NUM_CUSTOMERS = 1000
NUM_POLICIES = 1500
NUM_CLAIMS = 500

def generate_mock_data():
    """Generates thousands of realistic records to stress-test the database."""
    print("🚀 Starting Data Pipeline Injection...")
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # --- 1. GENERATE CUSTOMERS ---
        print(f"Generating {NUM_CUSTOMERS} Customers...")
        customers_data = []
        for _ in range(NUM_CUSTOMERS):
            customers_data.append((
                fake.first_name(),
                fake.last_name(),
                fake.unique.email(),
                fake.phone_number()[:15], # Keep it within reasonable length
                fake.address().replace('\n', ', ') # Flatten addresses
            ))
        
        # Use executemany for high-performance bulk inserts
        cursor.executemany("""
            INSERT INTO customers (first_name, last_name, email, phone, address)
            VALUES (?, ?, ?, ?, ?)
        """, customers_data)
        conn.commit()

        # --- 2. GENERATE POLICIES ---
        print(f"Generating {NUM_POLICIES} Policies...")
        # Get valid customer and type IDs to map policies to
        cursor.execute("SELECT customer_id FROM customers")
        customer_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT type_id FROM policy_types")
        type_ids = [row[0] for row in cursor.fetchall()]

        policies_data = []
        for _ in range(NUM_POLICIES):
            start_date = fake.date_between(start_date='-3y', end_date='today')
            end_date = start_date + timedelta(days=365)
            status = random.choices(['Active', 'Expired', 'Cancelled'], weights=[70, 20, 10])[0]
            
            policies_data.append((
                random.choice(customer_ids),
                random.choice(type_ids),
                f"POL-{secrets.token_hex(3).upper()}",
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
                round(random.uniform(500.0, 3000.0), 2),
                status
            ))

        cursor.executemany("""
            INSERT INTO policies (customer_id, type_id, policy_number, start_date, end_date, premium_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, policies_data)
        conn.commit()

        # --- 3. GENERATE CLAIMS, INCIDENTS & PAYMENTS ---
        print(f"Generating {NUM_CLAIMS} Claims and Incident Reports...")
        cursor.execute("SELECT policy_id FROM policies")
        policy_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(NUM_CLAIMS):
            pol_id = random.choice(policy_ids)
            date_filed = fake.date_between(start_date='-2y', end_date='today')
            status = random.choices(['Pending', 'Approved', 'Rejected'], weights=[20, 60, 20])[0]
            req_amount = round(random.uniform(1000.0, 50000.0), 2)
            
            # Logic: If approved, they get a random percentage of what they asked for
            appr_amount = round(req_amount * random.uniform(0.5, 1.0), 2) if status == 'Approved' else 0.0

            # Insert Claim
            cursor.execute("""
                INSERT INTO claims (policy_id, date_filed, status, claim_amount, approved_amount)
                VALUES (?, ?, ?, ?, ?)
            """, (pol_id, date_filed.strftime("%Y-%m-%d"), status, req_amount, appr_amount))
            claim_id = cursor.lastrowid

            # Insert Incident
            inc_date = date_filed - timedelta(days=random.randint(1, 14))
            cursor.execute("""
                INSERT INTO incidents (claim_id, incident_date, location, description)
                VALUES (?, ?, ?, ?)
            """, (
                claim_id, 
                inc_date.strftime("%Y-%m-%d"), 
                fake.city(), 
                fake.sentence(nb_words=10)
            ))

            # Insert Payment if Approved
            if status == 'Approved':
                pay_date = date_filed + timedelta(days=random.randint(5, 30))
                cursor.execute("""
                    INSERT INTO payments (policy_id, amount, payment_date, payment_type)
                    VALUES (?, ?, ?, 'Claim Payout')
                """, (pol_id, appr_amount, pay_date.strftime("%Y-%m-%d")))

        conn.commit()
        print("✅ Data Pipeline Injection Complete! Your database is now populated.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error generating data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    generate_mock_data()