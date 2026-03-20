# Global Insurance Management System

A robust, full-stack desktop application designed to streamline insurance operations. This system replaces manual spreadsheet processes with a centralized, encrypted database solution for managing policies, processing claims, and visualizing financial analytics.

## 🎯 Key Architecture & Features
* **Modern UI/UX:** Built with CustomTkinter for a responsive, grid-based, dark-mode interface with dynamic, centered modal windows.
* **Business Intelligence Dashboard:** Real-time KPI aggregation and embedded time-series data visualization (trailing 12-month claims) rendered natively using Matplotlib.
* **Relational Database Design:** Built on SQLite utilizing 3rd Normal Form (3NF) to ensure data integrity across Customers, Policies, and Claims.
* **Atomic Transactions:** Claims processing is handled via strict database transactions, ensuring an Incident Report and Financial Claim are either saved together or safely rolled back.
* **Synthetic Data Pipeline:** Includes a developer tool utilizing the Faker library to inject 3,000+ realistic, relationally mapped records to stress-test UI rendering and database indexing.
* **Enterprise-Grade Security:**
    * Role-Based Access Control (RBAC) separating Admins, Managers, and Staff.
    * Database encryption leveraging SQLCipher at rest.
    * Password hashing implemented with `bcrypt`.

## 🛠 Tech Stack
* **Language:** Python 3.12+
* **Frontend UI:** CustomTkinter
* **Data Visualization:** Matplotlib
* **Database:** SQLite 3 (with `pysqlcipher3` integration)
* **Data Engineering:** Faker
* **Security & Testing:** `bcrypt`, `unittest`

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Abrar-Khaleel/global-insurance-app.git
   cd global-insurance-app
   ```

2. **Activate your virtual environment and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the encrypted database and create an admin user:**
   ```bash
   python auth.py
   ```

4. **Generate the mock database (Highly Recommended):**
   *Run this script to inject thousands of realistic customers, policies, and claims so the Analytics Dashboard has data to visualize.*
   ```bash
   python generate_data.py
   ```

5. **Launch the application:**
   ```bash
   python main.py
   ```