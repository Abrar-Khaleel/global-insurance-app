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
        
        # 1. Header
        header_frame = ttk.Frame(self.content_area)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header_frame, text="Policy Management", font=("Arial", 18, "bold")).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="+ Create New Policy", command=self.open_add_policy_window).pack(side=tk.RIGHT)

        # 2. Policy List (Treeview)
        # Note: We display names, not IDs, for better UX
        columns = ("ID", "Policy #", "Customer", "Type", "Start", "End", "Premium", "Status")
        self.policy_tree = ttk.Treeview(self.content_area, columns=columns, show="headings")
        
        for col in columns:
            self.policy_tree.heading(col, text=col)
            width = 100 if col in ["Start", "End", "Status"] else 150
            self.policy_tree.column(col, width=width)
            
        self.policy_tree.column("ID", width=50)
        self.policy_tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_policy_list()

    def refresh_policy_list(self):
        for item in self.policy_tree.get_children():
            self.policy_tree.delete(item)
        
        policies = backend.get_all_policies()
        for pol in policies:
            self.policy_tree.insert("", tk.END, values=pol)

    def open_add_policy_window(self):
        policy_win = tk.Toplevel(self.root)
        policy_win.title("Create New Policy")
        policy_win.geometry("500x500")

        # --- Data Loading for Dropdowns ---
        # Get Customers: returns list of (id, first, last...)
        customers_raw = backend.get_all_customers() 
        # Create a dict to map "Name (ID)" string back to ID
        customer_map = {f"{c[1]} {c[2]} (ID: {c[0]})": c[0] for c in customers_raw}
        customer_options = list(customer_map.keys())

        # Get Policy Types
        types_raw = backend.get_policy_types()
        type_map = {f"{t[1]}": t[0] for t in types_raw}
        type_options = list(type_map.keys())

        # --- Form Fields ---
        
        # 1. Select Customer
        ttk.Label(policy_win, text="Select Customer:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        cust_combo = ttk.Combobox(policy_win, values=customer_options, state="readonly")
        cust_combo.pack(fill=tk.X, padx=20)

        # 2. Select Policy Type
        ttk.Label(policy_win, text="Policy Type:").pack(anchor=tk.W, padx=20, pady=(10, 5))
        type_combo = ttk.Combobox(policy_win, values=type_options, state="readonly")
        type_combo.pack(fill=tk.X, padx=20)

        # 3. Dates (Text Entry YYYY-MM-DD)
        ttk.Label(policy_win, text="Start Date (YYYY-MM-DD):").pack(anchor=tk.W, padx=20, pady=(10, 5))
        start_entry = ttk.Entry(policy_win)
        start_entry.insert(0, "2025-01-01") # Default value
        start_entry.pack(fill=tk.X, padx=20)

        ttk.Label(policy_win, text="End Date (YYYY-MM-DD):").pack(anchor=tk.W, padx=20, pady=(10, 5))
        end_entry = ttk.Entry(policy_win)
        end_entry.insert(0, "2026-01-01")
        end_entry.pack(fill=tk.X, padx=20)

        # 4. Premium
        ttk.Label(policy_win, text="Premium Amount ($):").pack(anchor=tk.W, padx=20, pady=(10, 5))
        premium_entry = ttk.Entry(policy_win)
        premium_entry.pack(fill=tk.X, padx=20)

        def save_policy():
            # Validation
            if not cust_combo.get() or not type_combo.get() or not premium_entry.get():
                tk.messagebox.showerror("Error", "All fields are required!")
                return
            
            # Map names back to IDs
            selected_cust_id = customer_map[cust_combo.get()]
            selected_type_id = type_map[type_combo.get()]
            
            success, msg = backend.add_policy(
                selected_cust_id, selected_type_id,
                start_entry.get(), end_entry.get(), premium_entry.get()
            )
            
            if success:
                tk.messagebox.showinfo("Success", msg)
                policy_win.destroy()
                self.refresh_policy_list()
            else:
                tk.messagebox.showerror("Error", msg)

        ttk.Button(policy_win, text="Create Policy", command=save_policy).pack(pady=30)
        
    def show_claims(self):
        self.clear_content()
        
        # 1. Header
        header = ttk.Frame(self.content_area)
        header.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header, text="Claims Processing", font=("Arial", 18, "bold")).pack(side=tk.LEFT)
        ttk.Button(header, text="+ File New Claim", command=self.open_file_claim_window).pack(side=tk.RIGHT)
        ttk.Button(header, text="Process Selected", command=self.open_process_claim_window).pack(side=tk.RIGHT, padx=10)

        # 2. Claims List (Treeview)
        columns = ("ID", "Policy #", "Customer", "Date Filed", "Amount ($)", "Status")
        self.claims_tree = ttk.Treeview(self.content_area, columns=columns, show="headings")
        
        for col in columns:
            self.claims_tree.heading(col, text=col)
            self.claims_tree.column(col, width=120)
        
        # Color Code the Status rows (Optional Visual Flair)
        self.claims_tree.tag_configure('Pending', foreground='orange')
        self.claims_tree.tag_configure('Approved', foreground='green')
        self.claims_tree.tag_configure('Rejected', foreground='red')

        self.claims_tree.pack(fill=tk.BOTH, expand=True)
        self.refresh_claims_list()

    def refresh_claims_list(self):
        for item in self.claims_tree.get_children():
            self.claims_tree.delete(item)
            
        claims = backend.get_all_claims()
        for cl in claims:
            # cl[5] is the status column index
            self.claims_tree.insert("", tk.END, values=cl, tags=(cl[5],))

    def open_process_claim_window(self):
        """Opens a window to approve or reject a selected claim."""
        # 1. Check if a row is selected
        selected = self.claims_tree.selection()
        if not selected:
            tk.messagebox.showwarning("Selection Required", "Please click on a claim in the list first.")
            return

        # 2. Get data from the selected row
        item = self.claims_tree.item(selected[0])
        values = item['values']
        claim_id = values[0]
        req_amount = values[4]
        current_status = values[5]

        # 3. Prevent processing already completed claims
        if current_status != 'Pending':
            tk.messagebox.showinfo("Notice", f"This claim has already been {current_status}.")
            return

        # 4. Build the popup window
        process_win = tk.Toplevel(self.root)
        process_win.title(f"Process Claim #{claim_id}")
        process_win.geometry("350x200")

        ttk.Label(process_win, text=f"Requested Amount: ${req_amount}", font=("Arial", 12, "bold")).pack(pady=15)

        ttk.Label(process_win, text="Approved Amount ($):").pack(anchor=tk.W, padx=20)
        appr_amount_entry = ttk.Entry(process_win)
        appr_amount_entry.insert(0, req_amount) # Default to fully approving the requested amount
        appr_amount_entry.pack(fill=tk.X, padx=20, pady=5)

        def finalize(status):
            # If rejected, override the entry to 0.0
            final_amt = 0.0 if status == 'Rejected' else appr_amount_entry.get()
            
            success, msg = backend.process_claim(claim_id, status, final_amt)
            if success:
                tk.messagebox.showinfo("Success", msg)
                process_win.destroy()
                self.refresh_claims_list() # Updates the table colors immediately
            else:
                tk.messagebox.showerror("Error", msg)

        # Buttons Frame
        btn_frame = ttk.Frame(process_win)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Approve", command=lambda: finalize('Approved')).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Reject", command=lambda: finalize('Rejected')).pack(side=tk.LEFT, padx=10)

    def open_file_claim_window(self):
        claim_win = tk.Toplevel(self.root)
        claim_win.title("File New Claim")
        claim_win.geometry("600x600")

        # --- Load Policies for Dropdown ---
        policies = backend.get_active_policies()
        # Create map: "Policy # - Customer Name" -> ID
        policy_map = {f"{p[1]} - {p[2]} {p[3]}": p[0] for p in policies}
        
        if not policy_map:
            tk.messagebox.showerror("Error", "No Active Policies found. Create a policy first.")
            claim_win.destroy()
            return

        # --- Form Layout ---
        
        # Section 1: Policy Info
        ttk.Label(claim_win, text="Select Policy:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=20, pady=(20, 5))
        policy_combo = ttk.Combobox(claim_win, values=list(policy_map.keys()), state="readonly", width=50)
        policy_combo.pack(padx=20)

        # Section 2: Financials
        ttk.Label(claim_win, text="Claim Amount ($):", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 5))
        amount_entry = ttk.Entry(claim_win)
        amount_entry.pack(fill=tk.X, padx=20)

        ttk.Label(claim_win, text="Date Filed (YYYY-MM-DD):", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=20, pady=(10, 5))
        date_entry = ttk.Entry(claim_win)
        date_entry.insert(0, "2026-01-25")
        date_entry.pack(fill=tk.X, padx=20)

        # Section 3: Incident Details (The "Story")
        ttk.Separator(claim_win, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        ttk.Label(claim_win, text="Incident Report Details", font=("Arial", 12, "bold")).pack(pady=(0, 10))

        ttk.Label(claim_win, text="Incident Date (YYYY-MM-DD):").pack(anchor=tk.W, padx=20)
        inc_date_entry = ttk.Entry(claim_win)
        inc_date_entry.insert(0, "2026-01-24")
        inc_date_entry.pack(fill=tk.X, padx=20, pady=5)

        ttk.Label(claim_win, text="Incident Location:").pack(anchor=tk.W, padx=20)
        location_entry = ttk.Entry(claim_win)
        location_entry.pack(fill=tk.X, padx=20, pady=5)

        ttk.Label(claim_win, text="Description of Incident:").pack(anchor=tk.W, padx=20)
        # Using Text widget for multi-line description
        desc_entry = tk.Text(claim_win, height=5, width=50)
        desc_entry.pack(padx=20, pady=5)

        def submit_claim():
            if not policy_combo.get() or not amount_entry.get():
                tk.messagebox.showerror("Error", "Policy and Amount are required.")
                return

            pol_id = policy_map[policy_combo.get()]
            description = desc_entry.get("1.0", tk.END).strip() # Get text from Text widget
            
            success, msg = backend.file_claim(
                pol_id, date_entry.get(), amount_entry.get(),
                inc_date_entry.get(), location_entry.get(), description
            )

            if success:
                tk.messagebox.showinfo("Success", msg)
                claim_win.destroy()
                self.refresh_claims_list()
            else:
                tk.messagebox.showerror("Error", msg)

        ttk.Button(claim_win, text="Submit Claim Request", command=submit_claim).pack(pady=20)


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