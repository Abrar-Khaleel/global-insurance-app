import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import auth  
from views import Dashboard

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Insurance Inc. - Login")
        self.root.geometry("400x350")
        
        # Center the window on the screen
        self.center_window()

        # --- UI Styling ---
        # Create a clean layout using a Frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Title Label
        title_label = ttk.Label(
            main_frame, 
            text="Staff Login", 
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=(10, 20))

        # Username Field
        ttk.Label(main_frame, text="Username").pack(anchor="w")
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.pack(fill="x", pady=(5, 15))

        # Password Field
        ttk.Label(main_frame, text="Password").pack(anchor="w")
        self.password_entry = ttk.Entry(main_frame, show="*") # Hides text
        self.password_entry.pack(fill="x", pady=(5, 20))

        # Login Button
        login_btn = ttk.Button(
            main_frame, 
            text="Login", 
            command=self.perform_login
        )
        login_btn.pack(fill="x", pady=5)

        # Status Label (For error messages)
        self.status_label = ttk.Label(main_frame, text="", foreground="red")
        self.status_label.pack(pady=10)

    def center_window(self):
        """Calculates center point of screen to place window."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def perform_login(self):
            """Handles the login logic connecting to the database."""
            username = self.username_entry.get()
            password = self.password_entry.get()

            if not username or not password:
                self.status_label.config(text="Please enter both fields.")
                return

            role = auth.login_user(username, password)
            
            if role:
                messagebox.showinfo("Success", f"Welcome back, {role}!") 
                self.open_dashboard(role) # Open the main app
            else:
                self.status_label.config(text="Invalid credentials.")
                self.password_entry.delete(0, tk.END)

    def open_dashboard(self, role):
            self.root.destroy() # Close login
            new_root = tk.Tk()  # Create new window for dashboard
            app = Dashboard(new_root, role)
            new_root.mainloop()

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    
    # Apply a theme (built-in to Mac/Windows) for better looks
    style = ttk.Style()
    style.theme_use('aqua') # 'clam' is often cleaner, on Mac try 'aqua' or 'alt'
    
    app = LoginWindow(root)
    root.mainloop()