import tkinter as tk
from tkinter import ttk
import backend

class Dashboard:
    def __init__(self, root, role):
        self.root = root
        self.role = role
        self.root.title(f"Global Insurance Inc. - {role} Dashboard")
        self.root.geometry("1000x600")

        # --- STYLE CONFIGURATION ---
        style = ttk.Style()
        style.configure("Sidebar.TFrame", background="#E1E1E1")
        style.configure("Sidebar.TButton", font=("Arial", 12), padding=10)
        
        # --- MAIN LAYOUT ---
        # We use a PanedWindow to separate the Sidebar (Left) from Content (Right)
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # 1. SIDEBAR (Navigation)
        self.sidebar = ttk.Frame(self.paned_window, style="Sidebar.TFrame", width=200)
        self.paned_window.add(self.sidebar)

        # 2. CONTENT AREA (Where forms/tables will appear)
        self.content_area = ttk.Frame(self.paned_window, padding=20)
        self.paned_window.add(self.content_area)

        # --- NAVIGATION BUTTONS ---
        # We store buttons in a list to manage them easily
        self.nav_buttons = [
            ("Home", self.show_home),
            ("Manage Policies", self.show_policies),
            ("Manage Claims", self.show_claims),
            ("Customers", self.show_customers),
            ("Logout", self.logout)
        ]

        for text, command in self.nav_buttons:
            btn = ttk.Button(self.sidebar, text=text, command=command, style="Sidebar.TButton")
            btn.pack(fill=tk.X, pady=5, padx=5)

        # Load the Home screen by default
        self.show_home()

    def clear_content(self):
        """Removes all widgets from the content area before showing a new page."""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- PAGE VIEWS ---
    
    def show_home(self):
        self.clear_content()
        ttk.Label(self.content_area, text=f"Welcome, {self.role}!", font=("Arial", 24)).pack(pady=20)
        ttk.Label(self.content_area, text="Select an option from the sidebar to begin.").pack()
        
        # Example: Quick Stats (Professional touch)
        stats_frame = ttk.Frame(self.content_area)
        stats_frame.pack(pady=30, fill=tk.X)
        
        # Dummy stats for now
        ttk.Label(stats_frame, text="Pending Claims: 12", foreground="red", font=("Arial", 14)).pack(side=tk.LEFT, padx=20)
        ttk.Label(stats_frame, text="Active Policies: 145", foreground="green", font=("Arial", 14)).pack(side=tk.LEFT, padx=20)

    def show_policies(self):
        self.clear_content()
        ttk.Label(self.content_area, text="Policy Management", font=("Arial", 18, "bold")).pack(anchor=tk.W, pady=(0, 20))
        # We will add the policy table/form here later
        ttk.Button(self.content_area, text="+ Create New Policy").pack(anchor=tk.W)

    def show_claims(self):
        self.clear_content()
        ttk.Label(self.content_area, text="Claims Processing", font=("Arial", 18, "bold")).pack(anchor=tk.W, pady=(0, 20))
        # We will add claims logic here later

    # ... inside Dashboard class ...

    def show_customers(self):
        self.clear_content()
        
        # 1. Header Area
        header_frame = ttk.Frame(self.content_area)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Customer Directory", font=("Arial", 18, "bold")).pack(side=tk.LEFT)
        
        # Add Customer Button
        ttk.Button(header_frame, text="+ Add New Customer", command=self.open_add_customer_window).pack(side=tk.RIGHT)

        # 2. Search Bar
        search_frame = ttk.Frame(self.content_area)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search by Last Name:").pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(search_frame, text="Search", command=self.perform_search).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Reset", command=self.refresh_customer_list).pack(side=tk.LEFT, padx=10)

        # 3. Customer List (Treeview)
        columns = ("ID", "First Name", "Last Name", "Email", "Phone")
        self.tree = ttk.Treeview(self.content_area, columns=columns, show="headings")
        
        # Define Headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150) # Adjust width as needed
            
        self.tree.column("ID", width=50) # Make ID column smaller
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Load initial data
        self.refresh_customer_list()

    def refresh_customer_list(self):
        """Clears the table and reloads all data from backend."""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Fetch from database
        customers = backend.get_all_customers()
        for cust in customers:
            self.tree.insert("", tk.END, values=cust)

    def perform_search(self):
        query = self.search_entry.get()
        if not query:
            return
            
        # Clear and fetch search results
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        results = backend.search_customers(query)
        for res in results:
            self.tree.insert("", tk.END, values=res)

    def open_add_customer_window(self):
        """Opens a pop-up window to add a customer."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Customer")
        add_window.geometry("400x400")
        
        # Form Fields
        ttk.Label(add_window, text="First Name:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        fname_entry = ttk.Entry(add_window)
        fname_entry.pack(fill=tk.X, padx=20)

        ttk.Label(add_window, text="Last Name:").pack(anchor=tk.W, padx=20, pady=(10, 5))
        lname_entry = ttk.Entry(add_window)
        lname_entry.pack(fill=tk.X, padx=20)

        ttk.Label(add_window, text="Email:").pack(anchor=tk.W, padx=20, pady=(10, 5))
        email_entry = ttk.Entry(add_window)
        email_entry.pack(fill=tk.X, padx=20)

        ttk.Label(add_window, text="Phone:").pack(anchor=tk.W, padx=20, pady=(10, 5))
        phone_entry = ttk.Entry(add_window)
        phone_entry.pack(fill=tk.X, padx=20)
        
        ttk.Label(add_window, text="Address:").pack(anchor=tk.W, padx=20, pady=(10, 5))
        address_entry = ttk.Entry(add_window)
        address_entry.pack(fill=tk.X, padx=20)

        def save_action():
            success, message = backend.add_customer(
                fname_entry.get(), lname_entry.get(), 
                email_entry.get(), phone_entry.get(), address_entry.get()
            )
            if success:
                tk.messagebox.showinfo("Success", message)
                add_window.destroy()
                self.refresh_customer_list() # Update the list behind the window
            else:
                tk.messagebox.showerror("Error", message)

        ttk.Button(add_window, text="Save Customer", command=save_action).pack(pady=20)

    def logout(self):
        self.root.destroy()
        # In a real app, this would re-open the LoginWindow
        print("Logged out.")