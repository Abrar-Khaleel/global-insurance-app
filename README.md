# Global Insurance Management System

A robust desktop application designed to streamline insurance operations. This system replaces manual spreadsheet processes with a centralized, encrypted database solution for managing policies, claims, and customer data. 

## 🎯 Key Architecture & Features
* **Relational Database Design:** Built on SQLite utilizing 3rd Normal Form (3NF) to ensure data integrity across Customers, Policies, and Claims.
* **Atomic Transactions:** Claims processing is handled via database transactions, ensuring an Incident Report and Financial Claim are either saved together or safely rolled back.
* **Enterprise-Grade Security:**
    * Role-Based Access Control (RBAC) separating Admins, Managers, and Staff.
    * Database encryption leveraging SQLCipher.
    * Password hashing implemented with `bcrypt`.
* **Financial Ledger:** Automated payment generation upon claim approval with real-time reporting dashboards.
* **Separation of Concerns:** Clean MVC-inspired architecture separating database logic (`backend.py`) from GUI rendering (`views.py`).
* **Automated Testing:** Core security modules verified via unit testing.

## 🛠 Tech Stack
* **Language:** Python 3.11+
* **Database:** SQLite 3 (with SQLCipher integration)
* **GUI:** Tkinter (Themed)
* **Testing & Security:** `unittest`, `bcrypt`, `pysqlcipher3`

## 🚀 Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/Abrar-Khaleel/global-insurance-app.git
   ```
2. Activate your virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database and create an admin user:
   ```bash
   python auth.py
   ```
4. Launch the application:
   ```bash
   python main.py
   ```