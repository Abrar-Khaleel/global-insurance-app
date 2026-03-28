import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import backend

class Dashboard:
    def __init__(self, root, role):
        self.root = root
        self.role = role
        self.root.title(f"Global Insurance Inc. - {role} Dashboard v2.0")

        # --- GRID LAYOUT SETUP ---
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # 1. SIDEBAR (Fixed Width)
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1) # Pushes logout to the bottom

        # Sidebar Title
        ctk.CTkLabel(self.sidebar, text="Global Ins.", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 30))

        # 2. CONTENT AREA (Dynamic)
        # using fg_color="transparent" so it blends with the main window background
        self.content_area = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # --- NAVIGATION BUTTONS ---
        self.nav_buttons = [
            ("Dashboard", self.show_home),
            ("Manage Policies", self.show_policies),
            ("Manage Claims", self.show_claims),
            ("Customers", self.show_customers),
            ("Financial Reports", self.show_reports),
        ]

        # Render Main Nav Buttons
        for idx, (text, command) in enumerate(self.nav_buttons, start=1):
            btn = ctk.CTkButton(self.sidebar, text=text, command=command, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
            btn.grid(row=idx, column=0, pady=5, padx=20, sticky="ew")

        # Logout Button at the bottom
        logout_btn = ctk.CTkButton(self.sidebar, text="Logout", command=self.logout, fg_color="#ff4d4d", hover_color="#cc0000")
        logout_btn.grid(row=9, column=0, pady=20, padx=20, sticky="ew")

        # Apply custom styling to the standard ttk.Treeview
        self.apply_treeview_style()

        # Load the Home screen by default
        self.show_home()

    def apply_treeview_style(self):
        """Forces the standard Tkinter Treeview to look like a modern Dark Mode widget."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        rowheight=30,
                        fieldbackground="#2b2b2b",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=("Arial", 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading",
                        background="#343638",
                        foreground="white",
                        relief="flat",
                        font=("Arial", 12, "bold"))
        style.map("Treeview.Heading", background=[('active', '#3484F0')])
    
    def center_toplevel(self, window, width, height):
        """Calculates the exact center of the screen to spawn a pop-up window."""
        self.root.update_idletasks() # Ensure the main window is fully rendered first
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def clear_content(self):
        """Removes all widgets from the content area before showing a new page."""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- PAGE VIEWS ---
    
    def show_home(self):
        self.clear_content()
        
        # 1. Welcome Header
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header_frame, text=f"Welcome, {self.role}!", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left")

        # Fetch Analytics Data from Backend
        premium, payouts, rate = backend.get_analytics_kpis()
        
        # 2. KPI Cards (Top Row)
        kpi_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=(0, 20))

        def create_kpi_card(parent, title, value, color):
            # 1. Remove 'padding' from the Frame creation
            card = ctk.CTkFrame(parent, corner_radius=10)
            card.pack(side="left", fill="x", expand=True, padx=10)
            
            # 2. Add padx and pady to the labels to create the internal spacing
            ctk.CTkLabel(card, text=title, text_color="gray", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(20, 0))
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=26, weight="bold"), text_color=color).pack(anchor="w", padx=20, pady=(5, 20))

        create_kpi_card(kpi_frame, "Active Premiums", f"${premium:,.2f}", "#00cc66")
        create_kpi_card(kpi_frame, "Total Payouts", f"${payouts:,.2f}", "#ff4d4d")
        create_kpi_card(kpi_frame, "Approval Rate", f"{rate:.1f}%", "#3399ff")

        # 3. Analytics Chart (Bottom Area)
        chart_frame = ctk.CTkFrame(self.content_area, corner_radius=10)
        chart_frame.pack(fill="both", expand=True, padx=5, pady=5)

        chart_data = backend.get_claims_by_month()
        
        if chart_data:
            months = [row[0] for row in chart_data]
            counts = [row[1] for row in chart_data]

            fig = Figure(figsize=(8, 4), dpi=100, facecolor='#2b2b2b')
            ax = fig.add_subplot(111)
            ax.set_facecolor('#2b2b2b')
            ax.bar(months, counts, color='#4da6ff')
            
            ax.set_title("Claims Filed (Trailing 12 Months)", fontsize=14, color='white', pad=15)
            ax.set_ylabel("Volume of Claims", fontsize=10, color='white')
            
            ax.tick_params(axis='x', rotation=45, colors='white', labelcolor='white')
            ax.tick_params(axis='y', colors='white', labelcolor='white')
            for spine in ax.spines.values():
                spine.set_edgecolor('white')
            
            fig.tight_layout()

            # Embed the Figure into Tkinter/CustomTkinter
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        else:
            ctk.CTkLabel(chart_frame, text="Not enough data to generate chart.", text_color="gray").pack(pady=40)

    def show_policies(self):
        self.clear_content()
        
        # Header Area
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header_frame, text="Policy Management", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        
        # Primary Action Button
        ctk.CTkButton(header_frame, text="+ Create New Policy", font=ctk.CTkFont(weight="bold"), 
                      fg_color="#00cc66", hover_color="#00994d", command=self.open_add_policy_window).pack(side="right")

        # Treeview Container (Added padding for breathing room)
        tree_frame = ctk.CTkFrame(self.content_area, corner_radius=10)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("ID", "Policy #", "Customer", "Type", "Start", "End", "Premium", "Status")
        self.policy_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.policy_tree.heading(col, text=col)
            width = 100 if col in ["Start", "End", "Status"] else 150
            self.policy_tree.column(col, width=width)
            
        self.policy_tree.column("ID", width=50)
        self.policy_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_policy_list()

    def show_reports(self):
        self.clear_content()
        
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header_frame, text="Financial & Ledger Reports", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")

        tree_frame = ctk.CTkFrame(self.content_area, corner_radius=10)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("Transaction ID", "Policy #", "Customer", "Type", "Amount ($)", "Date")
        self.reports_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.reports_tree.heading(col, text=col)
            self.reports_tree.column(col, width=120)
            
        self.reports_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        records = backend.get_financial_reports()
        for rec in records:
            self.reports_tree.insert("", tk.END, values=rec)
            
        total_payouts = sum(float(rec[4]) for rec in records if rec[3] == 'Claim Payout')
        
        # Styled Summary Card
        summary_frame = ctk.CTkFrame(self.content_area, fg_color="#331a1a", border_width=1, border_color="#ff4d4d")
        summary_frame.pack(fill="x", pady=(20, 0), padx=5)
        ctk.CTkLabel(summary_frame, text=f"Total Claim Payouts To Date: ${total_payouts:,.2f}", 
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#ff4d4d").pack(side="right", padx=20, pady=15)

    def refresh_policy_list(self):
        for item in self.policy_tree.get_children():
            self.policy_tree.delete(item)
        for pol in backend.get_all_policies():
            self.policy_tree.insert("", tk.END, values=pol)

    def open_add_policy_window(self):
        policy_win = ctk.CTkToplevel(self.root)
        policy_win.title("Create New Policy")
        self.center_toplevel(policy_win, 500, 680)
        policy_win.grab_set()

        # Center Title
        ctk.CTkLabel(policy_win, text="Policy Details", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        customers_raw = backend.get_all_customers() 
        customer_map = {f"{c[1]} {c[2]} (ID: {c[0]})": c[0] for c in customers_raw}
        customer_options = list(customer_map.keys())

        types_raw = backend.get_policy_types()
        type_map = {f"{t[1]}": t[0] for t in types_raw}
        type_options = list(type_map.keys())

        # Form Inputs with improved padding and heights
        ctk.CTkLabel(policy_win, text="Select Customer:", text_color="gray90").pack(anchor="w", padx=40, pady=(10, 2))
        cust_combo = ctk.CTkComboBox(policy_win, values=customer_options, height=35)
        cust_combo.pack(fill="x", padx=40)

        ctk.CTkLabel(policy_win, text="Policy Type:", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        type_combo = ctk.CTkComboBox(policy_win, values=type_options, height=35)
        type_combo.pack(fill="x", padx=40)

        ctk.CTkLabel(policy_win, text="Start Date (YYYY-MM-DD):", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        start_entry = ctk.CTkEntry(policy_win, height=35)
        start_entry.insert(0, "2025-01-01")
        start_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(policy_win, text="End Date (YYYY-MM-DD):", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        end_entry = ctk.CTkEntry(policy_win, height=35)
        end_entry.insert(0, "2026-01-01")
        end_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(policy_win, text="Premium Amount ($):", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        premium_entry = ctk.CTkEntry(policy_win, height=35)
        premium_entry.pack(fill="x", padx=40)

        def save_policy():
            if not cust_combo.get() or not type_combo.get() or not premium_entry.get():
                messagebox.showerror("Error", "All fields are required!")
                return
            
            selected_cust_id = customer_map[cust_combo.get()]
            selected_type_id = type_map[type_combo.get()]
            
            success, msg = backend.add_policy(
                selected_cust_id, selected_type_id,
                start_entry.get(), end_entry.get(), premium_entry.get()
            )
            
            if success:
                messagebox.showinfo("Success", msg)
                policy_win.destroy()
                self.refresh_policy_list()
            else:
                messagebox.showerror("Error", msg)

        ctk.CTkButton(policy_win, text="Save Policy", font=ctk.CTkFont(weight="bold"), height=40,
                      fg_color="#00cc66", hover_color="#00994d", command=save_policy).pack(pady=(30, 20), padx=40, fill="x")
        
    def show_claims(self):
        self.clear_content()
        
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header_frame, text="Claims Processing", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        
        # Action Buttons
        ctk.CTkButton(header_frame, text="+ File New Claim", font=ctk.CTkFont(weight="bold"),
                      fg_color="#00cc66", hover_color="#00994d", command=self.open_file_claim_window).pack(side="right")
        ctk.CTkButton(header_frame, text="Process Selected", font=ctk.CTkFont(weight="bold"),
                      fg_color="#3399ff", hover_color="#287acc", command=self.open_process_claim_window).pack(side="right", padx=10)

        tree_frame = ctk.CTkFrame(self.content_area, corner_radius=10)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("ID", "Policy #", "Customer", "Date Filed", "Amount ($)", "Status")
        self.claims_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.claims_tree.heading(col, text=col)
            self.claims_tree.column(col, width=120)
        
        self.claims_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_claims_list()

    def refresh_claims_list(self):
        for item in self.claims_tree.get_children():
            self.claims_tree.delete(item)
        for cl in backend.get_all_claims():
            self.claims_tree.insert("", tk.END, values=cl)

    def open_process_claim_window(self):
        selected = self.claims_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please click on a claim in the list first.")
            return

        item = self.claims_tree.item(selected[0])
        values = item['values']
        claim_id, req_amount, current_status = values[0], values[4], values[5]

        if current_status != 'Pending':
            messagebox.showinfo("Notice", f"This claim has already been {current_status}.")
            return

        process_win = ctk.CTkToplevel(self.root)
        process_win.title(f"Process Claim #{claim_id}")
        self.center_toplevel(process_win, 400, 250)
        process_win.grab_set()

        ctk.CTkLabel(process_win, text=f"Requested Amount: ${req_amount}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25, 15))

        ctk.CTkLabel(process_win, text="Approved Amount ($):", text_color="gray90").pack(anchor="w", padx=40)
        appr_amount_entry = ctk.CTkEntry(process_win, height=35)
        appr_amount_entry.insert(0, req_amount) 
        appr_amount_entry.pack(fill="x", padx=40, pady=5)

        def finalize(status):
            final_amt = 0.0 if status == 'Rejected' else appr_amount_entry.get()
            success, msg = backend.process_claim(claim_id, status, final_amt)
            if success:
                messagebox.showinfo("Success", msg)
                process_win.destroy()
                self.refresh_claims_list() 
            else:
                messagebox.showerror("Error", msg)

        btn_frame = ctk.CTkFrame(process_win, fg_color="transparent")
        btn_frame.pack(pady=20, fill="x", padx=40)

        ctk.CTkButton(btn_frame, text="Approve", font=ctk.CTkFont(weight="bold"), height=35,
                      fg_color="#00cc66", hover_color="#00994d", command=lambda: finalize('Approved')).pack(side="left", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text="Reject", font=ctk.CTkFont(weight="bold"), height=35,
                      fg_color="#ff4d4d", hover_color="#cc0000", command=lambda: finalize('Rejected')).pack(side="left", expand=True, padx=(5, 0))

    def open_file_claim_window(self):
        claim_win = ctk.CTkToplevel(self.root)
        claim_win.title("File New Claim")
        self.center_toplevel(claim_win, 600, 780)
        claim_win.grab_set()

        policies = backend.get_active_policies()
        policy_map = {f"{p[1]} - {p[2]} {p[3]}": p[0] for p in policies}
        
        if not policy_map:
            messagebox.showerror("Error", "No Active Policies found. Create a policy first.")
            claim_win.destroy()
            return
        
        ctk.CTkLabel(claim_win, text="New Claim Request", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
        
        ctk.CTkLabel(claim_win, text="Select Policy:", text_color="gray90").pack(anchor="w", padx=40, pady=(10, 2))
        policy_combo = ctk.CTkComboBox(claim_win, values=list(policy_map.keys()), height=35)
        policy_combo.pack(fill="x", padx=40)

        ctk.CTkLabel(claim_win, text="Claim Amount ($):", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        amount_entry = ctk.CTkEntry(claim_win, height=35)
        amount_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(claim_win, text="Date Filed (YYYY-MM-DD):", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        date_entry = ctk.CTkEntry(claim_win, height=35)
        date_entry.insert(0, "2026-01-25")
        date_entry.pack(fill="x", padx=40)

        # Separator for Incident Details
        ctk.CTkFrame(claim_win, height=2, fg_color="#343638").pack(fill="x", padx=40, pady=25)
        ctk.CTkLabel(claim_win, text="Incident Details", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=40, pady=(0, 10))

        ctk.CTkLabel(claim_win, text="Incident Date (YYYY-MM-DD):", text_color="gray90").pack(anchor="w", padx=40)
        inc_date_entry = ctk.CTkEntry(claim_win, height=35)
        inc_date_entry.insert(0, "2026-01-24")
        inc_date_entry.pack(fill="x", padx=40, pady=5)

        ctk.CTkLabel(claim_win, text="Location:", text_color="gray90").pack(anchor="w", padx=40)
        location_entry = ctk.CTkEntry(claim_win, height=35)
        location_entry.pack(fill="x", padx=40, pady=5)

        ctk.CTkLabel(claim_win, text="Description:", text_color="gray90").pack(anchor="w", padx=40)
        desc_entry = ctk.CTkTextbox(claim_win, height=80)
        desc_entry.pack(fill="x", padx=40, pady=5)

        def submit_claim():
            if not policy_combo.get() or not amount_entry.get():
                messagebox.showerror("Error", "Policy and Amount are required.")
                return

            pol_id = policy_map[policy_combo.get()]
            description = desc_entry.get("0.0", "end").strip() 
            
            success, msg = backend.file_claim(
                pol_id, date_entry.get(), amount_entry.get(),
                inc_date_entry.get(), location_entry.get(), description
            )

            if success:
                messagebox.showinfo("Success", msg)
                claim_win.destroy()
                self.refresh_claims_list()
            else:
                messagebox.showerror("Error", msg)

        ctk.CTkButton(claim_win, text="Submit Request", font=ctk.CTkFont(weight="bold"), height=40,
                      fg_color="#00cc66", hover_color="#00994d", command=submit_claim).pack(pady=(20, 20), padx=40, fill="x")

    def show_customers(self):
        self.clear_content()
        
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header_frame, text="Customer Directory", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        
        ctk.CTkButton(header_frame, text="+ Add New Customer", font=ctk.CTkFont(weight="bold"),
                      fg_color="#00cc66", hover_color="#00994d", command=self.open_add_customer_window).pack(side="right")
        ctk.CTkButton(header_frame, text="Edit Selected", font=ctk.CTkFont(weight="bold"),
                      fg_color="transparent", border_width=1, hover_color="#343638", command=self.open_edit_customer_window).pack(side="right", padx=10)

        # Modern Search Bar Layout
        search_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(search_frame, width=250, placeholder_text="Search by Last Name...")
        self.search_entry.pack(side="left", padx=(0, 10))
        ctk.CTkButton(search_frame, text="Search", width=100, command=self.perform_search).pack(side="left")
        ctk.CTkButton(search_frame, text="Clear", width=100, fg_color="#4d4d4d", hover_color="#333333", command=self.refresh_customer_list).pack(side="left", padx=10)

        tree_frame = ctk.CTkFrame(self.content_area, corner_radius=10)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("ID", "First Name", "Last Name", "Email", "Phone")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150) 
            
        self.tree.column("ID", width=50) 
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_customer_list()

    def refresh_customer_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for cust in backend.get_all_customers():
            self.tree.insert("", tk.END, values=cust)

    def perform_search(self):
        query = self.search_entry.get()
        if not query:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        for res in backend.search_customers(query):
            self.tree.insert("", tk.END, values=res)

    def open_add_customer_window(self):
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("Add New Customer")
        self.center_toplevel(add_window, 450, 650)
        add_window.grab_set()

        ctk.CTkLabel(add_window, text="Customer Profile", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
        
        ctk.CTkLabel(add_window, text="First Name:", text_color="gray90").pack(anchor="w", padx=40, pady=(10, 2))
        fname_entry = ctk.CTkEntry(add_window, height=35)
        fname_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(add_window, text="Last Name:", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        lname_entry = ctk.CTkEntry(add_window, height=35)
        lname_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(add_window, text="Email:", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        email_entry = ctk.CTkEntry(add_window, height=35)
        email_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(add_window, text="Phone:", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        phone_entry = ctk.CTkEntry(add_window, height=35)
        phone_entry.pack(fill="x", padx=40)
        
        ctk.CTkLabel(add_window, text="Address:", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        address_entry = ctk.CTkEntry(add_window, height=35)
        address_entry.pack(fill="x", padx=40)

        def save_action():
            success, message = backend.add_customer(
                fname_entry.get(), lname_entry.get(), 
                email_entry.get(), phone_entry.get(), address_entry.get()
            )
            if success:
                messagebox.showinfo("Success", message)
                add_window.destroy()
                self.refresh_customer_list() 
            else:
                messagebox.showerror("Error", message)

        ctk.CTkButton(add_window, text="Save Customer", font=ctk.CTkFont(weight="bold"), height=40,
                      fg_color="#00cc66", hover_color="#00994d", command=save_action).pack(pady=(30, 20), padx=40, fill="x")
    
    def open_edit_customer_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please click on a customer in the list first.")
            return

        item = self.tree.item(selected[0])
        values = item['values']
        
        customer_id, curr_fname, curr_lname, curr_email, curr_phone = values[0], values[1], values[2], values[3], values[4]

        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title(f"Edit Customer #{customer_id}")
        self.center_toplevel(edit_window, 450, 650)
        edit_window.grab_set()

        ctk.CTkLabel(edit_window, text="Edit Profile", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
        
        ctk.CTkLabel(edit_window, text="First Name:", text_color="gray90").pack(anchor="w", padx=40, pady=(10, 2))
        fname_entry = ctk.CTkEntry(edit_window, height=35)
        fname_entry.insert(0, curr_fname)
        fname_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(edit_window, text="Last Name:", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        lname_entry = ctk.CTkEntry(edit_window, height=35)
        lname_entry.insert(0, curr_lname)
        lname_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(edit_window, text="Email:", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        email_entry = ctk.CTkEntry(edit_window, height=35)
        email_entry.insert(0, curr_email)
        email_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(edit_window, text="Phone:", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        phone_entry = ctk.CTkEntry(edit_window, height=35)
        phone_entry.insert(0, curr_phone if curr_phone != 'None' else '')
        phone_entry.pack(fill="x", padx=40)
        
        ctk.CTkLabel(edit_window, text="Address:", text_color="gray90").pack(anchor="w", padx=40, pady=(15, 2))
        address_entry = ctk.CTkEntry(edit_window, height=35)
        address_entry.pack(fill="x", padx=40)

        def save_changes():
            success, message = backend.update_customer(
                customer_id, fname_entry.get(), lname_entry.get(), 
                email_entry.get(), phone_entry.get(), address_entry.get()
            )
            if success:
                messagebox.showinfo("Success", message)
                edit_window.destroy()
                self.refresh_customer_list()
            else:
                messagebox.showerror("Error", message)

        ctk.CTkButton(edit_window, text="Update Profile", font=ctk.CTkFont(weight="bold"), height=40,
                      fg_color="#3399ff", hover_color="#287acc", command=save_changes).pack(pady=(30, 20), padx=40, fill="x")

    def logout(self):
        self.root.destroy()
        print("Logged out.")