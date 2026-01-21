import bcrypt
from db_setup import create_connection  # Reusing the connection logic we wrote earlier

def hash_password(plain_text_password):
    """
    Converts a plain text password into a secure hash using bcrypt.
    """
    # bcrypt requires bytes, so we encode the string
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def verify_password(plain_text_password, stored_hash):
    """
    Checks if a provided password matches the stored hash.
    Returns True if match, False otherwise.
    """
    try:
        # Check password against hash
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), stored_hash)
    except ValueError:
        return False

def register_user(username, password, role='Staff'):
    """
    Creates a new user in the database.
    Role options: 'Admin', 'Manager', 'Staff'
    """
    conn = create_connection()
    cursor = conn.cursor()
    
    # 1. Secure the password
    hashed_pw = hash_password(password)
    
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, hashed_pw, role))
        conn.commit()
        print(f"User '{username}' registered successfully as {role}.")
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False
    finally:
        conn.close()

def login_user(username, password):
    """
    Authenticates a user. Returns the user's Role if successful, or None if failed.
    """
    conn = create_connection()
    cursor = conn.cursor()
    
    # 1. Fetch the user's stored hash
    cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        stored_hash = result[0]
        user_role = result[1]
        
        # 2. Verify the password
        if verify_password(password, stored_hash):
            return user_role
    
    return None

# --- Quick Test Block ---
if __name__ == "__main__":
    # This block only runs if you run 'python auth.py' directly.
    # We will use this to create your first Admin account.
    
    print("--- Setting up Initial Admin User ---")
    admin_name = input("Enter new Admin username: ")
    admin_pass = input("Enter new Admin password: ")
    
    if register_user(admin_name, admin_pass, role='Admin'):
        print("Test Login...")
        role = login_user(admin_name, admin_pass)
        if role:
            print(f"Login Successful! Welcome, {role}.")
        else:
            print("Login Failed.")