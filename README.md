# Global Insurance Management System

A robust desktop application designed to streamline insurance operations. This system replaces manual spreadsheet processes with a centralized, encrypted database solution for managing policies, claims, and customer data.

## 🚧 Project Status
**Current State:** In Active Development 
**Latest Feature:** Database Architecture & User Authentication Module

## 🎯 Key Features
* **Centralized Database:** SQLite implementation with 3rd Normal Form (3NF) schema.
* **Security First:**
    * Role-Based Access Control (RBAC) for Admins, Managers, and Staff.
    * AES-256 Database Encryption using SQLCipher.
    * Password hashing with `bcrypt`.
* **Claims Processing:** (In Progress) Full lifecycle management from incident report to payout.

## 🛠 Tech Stack
* **Language:** Python 3.11+
* **Database:** SQLite 3 (with SQLCipher integration)
* **GUI:** Tkinter (Themed)
* **Security:** `bcrypt`, `pysqlcipher3`

## 🚀 Getting Started
1.  Clone the repository:
    ```bash
    git clone [https://github.com/Abrar-Khaleel/global-insurance-app.git](https://github.com/Abrar-Khaleel/global-insurance-app.git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Initialize the database:
    ```bash
    python db_setup.py
    ```