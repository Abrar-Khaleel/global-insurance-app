import customtkinter as ctk
from tkinter import messagebox
import auth  
from views import Dashboard

# --- CustomTkinter Global Settings ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Insurance Inc. - Login v2.0")
        self.root.geometry("450x450") # Slightly larger to accommodate modern padding
        
        # Center the window on the screen
        self.center_window()

        # --- UI Styling with CustomTkinter ---
        # Create a centered card layout
        main_frame = ctk.CTkFrame(root, corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=60, pady=60)

        # Title Label
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Staff Login", 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        )
        title_label.pack(pady=(30, 20))

        # Username Field (Using modern placeholders instead of separate labels)
        self.username_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Username",
            width=250,
            height=40
        )
        self.username_entry.pack(pady=(10, 15))

        # Password Field
        self.password_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="Password", 
            show="*",
            width=250,
            height=40
        )
        self.password_entry.pack(pady=(5, 20))

        # Login Button
        login_btn = ctk.CTkButton(
            main_frame, 
            text="Login", 
            command=self.perform_login,
            width=250,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        login_btn.pack(pady=10)

        # Status Label (For error messages)
        self.status_label = ctk.CTkLabel(main_frame, text="", text_color="#ff4d4d")
        self.status_label.pack(pady=10)

    def center_window(self):
        """Calculates center point of screen to place window."""
        self.root.update_idletasks()
        width = 450
        height = 450
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def perform_login(self):
        """Handles the login logic connecting to the database."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.status_label.configure(text="Please enter both fields.") # CTK uses .configure() instead of .config()
            return

        role = auth.login_user(username, password)
        
        if role:
            messagebox.showinfo("Success", f"Welcome back, {role}!") 
            self.open_dashboard(role) 
        else:
            self.status_label.configure(text="Invalid credentials.")
            self.password_entry.delete(0, 'end')

    def open_dashboard(self, role):
        self.root.destroy() # Close login
        new_root = ctk.CTk()  # Create new CustomTkinter window for dashboard
        app = Dashboard(new_root, role)
        new_root.mainloop()

if __name__ == "__main__":
    # Create the main CustomTkinter window
    root = ctk.CTk()
    app = LoginWindow(root)
    root.mainloop()