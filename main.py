import customtkinter as ctk
from tkinter import messagebox
import auth  
from views import Dashboard
import os
import json
from PIL import Image

# --- CustomTkinter Global Settings ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Insurance Inc. - Login v3.0")
        self.root.geometry("500x600") # Expanded to fit the V3 card layout
        
        # Center the window on the screen
        self.center_window(500, 600)

        # Clear any existing widgets (useful if reloading)
        for widget in self.root.winfo_children():
            widget.destroy()

        # --- Local Config for "Remember Me" ---
        self.config_file = "local_config.json"
        saved_username = ""
        is_remembered = False
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    saved_username = data.get("username", "")
                    is_remembered = data.get("remember", False)
            except Exception:
                pass

        # --- Main Login Card ---
        self.login_card = ctk.CTkFrame(self.root, width=350, height=480, corner_radius=15)
        self.login_card.place(relx=0.5, rely=0.5, anchor="center")
        self.login_card.pack_propagate(False) # Prevents card from shrinking

        # --- Company Branding ---
        ctk.CTkLabel(self.login_card, text="🛡️", font=ctk.CTkFont(size=45)).pack(pady=(35, 5))
        ctk.CTkLabel(self.login_card, text="Global Insurance", font=ctk.CTkFont(size=22, weight="bold")).pack()
        ctk.CTkLabel(self.login_card, text="Staff Portal v3.0", text_color="gray60", font=ctk.CTkFont(size=12)).pack(pady=(0, 30))

        # ==========================================
        # --- Username Input (Inner Icon Styling) ---
        # ==========================================
        # 1. The Frame acts as the visible "Input Box"
        self.user_frame = ctk.CTkFrame(self.login_card, border_width=2, border_color="#565B5E", fg_color="#343638", height=40, corner_radius=6)
        self.user_frame.pack(fill="x", padx=60, pady=(0, 15)) 
        
        # 2. Icon sits on the left side
        ctk.CTkLabel(self.user_frame, text="👤", font=ctk.CTkFont(size=16)).pack(side="left", padx=(10, 5))
        
        # 3. Entry is completely transparent and borderless
        self.username_entry = ctk.CTkEntry(self.user_frame, placeholder_text="Username", height=40, border_width=0, fg_color="transparent")
        self.username_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.username_entry.insert(0, saved_username)
        
        # 4. Focus State Binding (Highlights the *Frame*, not the Entry)
        self.username_entry.bind("<FocusIn>", lambda e: self.user_frame.configure(border_color="#3399ff"))
        self.username_entry.bind("<FocusOut>", lambda e: self.user_frame.configure(border_color="#565B5E"))

        # ==========================================
        # --- Password Input (Inner Icon Styling) ---
        # ==========================================
        self.pwd_frame = ctk.CTkFrame(self.login_card, border_width=2, border_color="#565B5E", fg_color="#343638", height=40, corner_radius=6)
        self.pwd_frame.pack(fill="x", padx=60, pady=(0, 10))
        
        ctk.CTkLabel(self.pwd_frame, text="🔒", font=ctk.CTkFont(size=16)).pack(side="left", padx=(10, 5))
        
        self.password_entry = ctk.CTkEntry(self.pwd_frame, placeholder_text="Password", height=40, show="*", border_width=0, fg_color="transparent")
        self.password_entry.pack(side="left", expand=True, fill="x")
        
        self.password_entry.bind("<FocusIn>", lambda e: self.pwd_frame.configure(border_color="#3399ff"))
        self.password_entry.bind("<FocusOut>", lambda e: self.pwd_frame.configure(border_color="#565B5E"))

        # Show/Hide Toggle Logic (Flipped Icons)
        def toggle_password():
            if self.password_entry.cget("show") == "*":
                self.password_entry.configure(show="")
                self.show_pwd_btn.configure(text="🙈") # Click to hide
            else:
                self.password_entry.configure(show="*")
                self.show_pwd_btn.configure(text="🐵") # Click to peek

        # Monkey sits on the right side of the frame
        self.show_pwd_btn = ctk.CTkButton(self.pwd_frame, text="🐵", width=30, height=30, fg_color="transparent", hover_color="#333333", command=toggle_password)
        self.show_pwd_btn.pack(side="right", padx=(0, 5))
        
        # --- Remember Me Checkbox ---
        self.remember_var = ctk.BooleanVar(value=is_remembered)
        ctk.CTkCheckBox(self.login_card, text="Remember Me", variable=self.remember_var, 
                        checkbox_height=18, checkbox_width=18, font=ctk.CTkFont(size=12)).pack(anchor="w", padx=60, pady=(0, 20)) 
        
        # --- Primary Action (Login Button) ---
        self.login_btn = ctk.CTkButton(self.login_card, text="Login", font=ctk.CTkFont(weight="bold"), 
                                       height=40, command=self.attempt_login)
        self.login_btn.pack(fill="x", padx=60, pady=(0, 15)) 

        # --- Forgot Password Link ---
        def forgot_password():
            messagebox.showinfo("Reset Password", "Please contact IT Support at helpdesk@globalins.com to reset your credentials.")
            
        ctk.CTkButton(self.login_card, text="Forgot Password?", font=ctk.CTkFont(size=12, underline=True),
                      fg_color="transparent", text_color="#3399ff", hover_color="#2b2b2b", command=forgot_password).pack()

        # --- Enter Key Workflow Routing ---
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.attempt_login())
        
        # Auto-focus logic on startup
        if saved_username:
            self.password_entry.focus()
        else:
            self.username_entry.focus()

    def center_window(self, width, height):
        """Calculates center point of screen to place window."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.trigger_shake_animation()
            return

        # 1. Trigger Loading State
        self.login_btn.configure(text="Authenticating...", state="disabled")
        self.root.update_idletasks() # Force UI repaint

        # 2. Simulate network delay, then verify via backend
        self.root.after(400, lambda: self.verify_and_route(username, password))

    def verify_and_route(self, username, password):
        """Handles the actual database check and routing."""
        role = auth.login_user(username, password)
        
        if role:
            # Handle Remember Me Configuration
            with open(self.config_file, "w") as f:
                json.dump({
                    "remember": self.remember_var.get(),
                    "username": username if self.remember_var.get() else ""
                }, f)
            
            self.open_dashboard(role) 
        else:
            # Reset Loading State and Shake
            self.login_btn.configure(text="Login", state="normal")
            self.password_entry.delete(0, "end")
            self.trigger_shake_animation()

    def trigger_shake_animation(self):
        """Creates a native macOS-style rejection shake on the login card."""
        offsets = [15, -15, 10, -10, 5, -5, 0] # Pixel offsets
        
        def step(index):
            if index < len(offsets):
                self.login_card.place(relx=0.5, rely=0.5, x=offsets[index], anchor="center")
                self.root.after(40, step, index + 1)
                
        step(0)

    def open_dashboard(self, role):
        # 1. Wipe the login screen clean
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title(f"Global Insurance Inc. - Admin Dashboard v3.0 ({role})")
        
        # 2. Load the Dashboard widgets FIRST
        app = Dashboard(self.root, role)
        
        # 3. Tell Tkinter to finish drawing the dashboard
        self.root.update_idletasks()
        
        # 4. NOW trigger the macOS Maximize!
        try:
            self.root.state('zoomed')
        except Exception:
            try:
                self.root.wm_attributes('-zoomed', 1)
            except Exception:
                w = self.root.winfo_screenwidth()
                h = self.root.winfo_screenheight()
                self.root.geometry(f"{w}x{h}+0+0")

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginWindow(root)
    root.mainloop()