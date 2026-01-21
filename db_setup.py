import os
# Try importing pysqlcipher3, fall back to standard sqlite3 if installation fails
# (This ensures you can still work even if encryption setup is tricky)
try:
    from pysqlcipher3 import dbapi2 as sqlite3
    ENCRYPTION_ACTIVE = True
    print("Security Module Loaded: SQLCipher")
except ImportError:
    import sqlite3
    ENCRYPTION_ACTIVE = False
    print("Warning: SQLCipher not found. Using standard SQLite (Unencrypted).")

DB_NAME = "global_insurance.db"
DB_PASSWORD = "SuperSecretPortfolioPassword123!"  # In production, use environment variables

def create_connection():
    """Connects to the database and enables encryption if available."""
    conn = sqlite3.connect(DB_NAME)
    if ENCRYPTION_ACTIVE:
        conn.execute(f"PRAGMA key = '{DB_PASSWORD}'")
    conn.execute("PRAGMA foreign_keys = 1") # Enforce strict relationships
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # 1. USERS TABLE (Role-Based Access Control)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT CHECK(role IN ('Admin', 'Manager', 'Staff')) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. CUSTOMERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        address TEXT
    );
    """)

    # 3. POLICY TYPES (Lookup Table)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS policy_types (
        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        default_coverage_amount REAL
    );
    """)

    # 4. POLICIES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS policies (
        policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        type_id INTEGER NOT NULL,
        policy_number TEXT UNIQUE NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        premium_amount REAL NOT NULL,
        status TEXT CHECK(status IN ('Active', 'Expired', 'Cancelled')) DEFAULT 'Active',
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
        FOREIGN KEY (type_id) REFERENCES policy_types (type_id)
    );
    """)

    # 5. CLAIMS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_id INTEGER NOT NULL,
        date_filed DATE NOT NULL,
        status TEXT CHECK(status IN ('Pending', 'Approved', 'Rejected')) DEFAULT 'Pending',
        claim_amount REAL NOT NULL,
        approved_amount REAL DEFAULT 0.0,
        FOREIGN KEY (policy_id) REFERENCES policies (policy_id)
    );
    """)

    # 6. INCIDENTS TABLE (1-to-1 link with Claims usually, or 1-to-Many)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        claim_id INTEGER NOT NULL,
        incident_date DATE NOT NULL,
        location TEXT NOT NULL,
        description TEXT NOT NULL,
        report_path TEXT,
        FOREIGN KEY (claim_id) REFERENCES claims (claim_id)
    );
    """)

    # 7. PAYMENTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_date DATE NOT NULL,
        payment_type TEXT CHECK(payment_type IN ('Premium', 'Claim Payout')),
        FOREIGN KEY (policy_id) REFERENCES policies (policy_id)
    );
    """)

    # Seed some initial Policy Types (so the app isn't empty)
    cursor.execute("INSERT OR IGNORE INTO policy_types (name, description, default_coverage_amount) VALUES ('Auto Comprehensive', 'Full coverage for vehicle accidents and theft', 50000.00)")
    cursor.execute("INSERT OR IGNORE INTO policy_types (name, description, default_coverage_amount) VALUES ('Home Fire', 'Coverage for fire damage to property', 250000.00)")

    conn.commit()
    conn.close()
    print("Database built successfully.")

if __name__ == "__main__":
    create_tables()