import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import random
import datetime
from db_utils import get_db_connection, hash_password, verify_password


# Premium Design Tokens (Glassmorphic Dark Aesthetic)
BG_PRIMARY = '#060314'      # Obsidian
BG_SECONDARY = '#0f0c24'    # Deep Indigo Panel
BG_INPUT = '#17123a'        # Translucent Navy Input
COLOR_TEXT = '#f8fafc'      # Slate White
COLOR_MUTED = '#94a3b8'     # Muted Grey-blue
COLOR_INDIGO = '#818cf8'    # Accent Indigo
COLOR_INDIGO_HOVER = '#6366f1'
COLOR_TEAL = '#2dd4bf'      # Accent Teal
COLOR_TEAL_HOVER = '#14b8a6'
COLOR_ROSE = '#f43f5e'      # Alert Rose

class VotingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Digital Voting Platform")
        self.root.geometry("850x650")
        self.root.configure(bg=BG_PRIMARY)
        
        # Database connection
        try:
            self.db = get_db_connection()
        except Exception as e:
            messagebox.showerror("Database Error", f"Connection failed: {str(e)}")
            self.root.destroy()
            return
        
        # Setup modern TTK styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
            "TScrollbar",
            gripcount=0,
            background=BG_INPUT,
            troughcolor=BG_PRIMARY,
            bordercolor=BG_PRIMARY,
            lightcolor=BG_PRIMARY,
            darkcolor=BG_PRIMARY
        )
        self.style.configure(
            "TCombobox",
            fieldbackground=BG_INPUT,
            background=BG_INPUT,
            foreground="white",
            bordercolor="#2b2654",
            arrowcolor=COLOR_TEAL
        )
        
        self.current_user = None
        self.show_main_menu()
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Display the main menu"""
        self.clear_window()
        self.root.configure(bg=BG_PRIMARY)
        
        # Title Card
        title_frame = tk.Frame(self.root, bg=BG_SECONDARY, height=120, highlightthickness=1, highlightbackground='#17123a')
        title_frame.pack(fill=tk.X, padx=25, pady=(25, 10))
        
        title_label = tk.Label(
            title_frame,
            text="SECURE DIGITAL VOTING PLATFORM",
            font=("Helvetica", 18, "bold"),
            bg=BG_SECONDARY,
            fg=COLOR_TEXT
        )
        title_label.pack(pady=(25, 5))
        
        subtitle_label = tk.Label(
            title_frame,
            text="State-of-the-Art Cryptographic Voting Registry",
            font=("Helvetica", 10),
            bg=BG_SECONDARY,
            fg=COLOR_MUTED
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=60, pady=25)
        
        buttons = [
            ("🔐 NEW VOTER SIGN UP", self.show_signup),
            ("📝 ACCESS VOTER LOGIN", self.show_login),
            ("🎯 PARTY REGISTRATION", self.show_party_registration),
            ("📊 REAL-TIME RESULTS", self.show_results),
            ("❌ EXIT SYSTEM", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Helvetica", 11, "bold"),
                bg=COLOR_INDIGO,
                fg='white',
                command=command,
                height=2,
                cursor="hand2",
                relief="flat",
                activebackground=COLOR_INDIGO_HOVER,
                activeforeground="white"
            )
            btn.pack(fill=tk.X, pady=8)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_INDIGO_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_INDIGO))
    
    def show_signup(self):
        """Display sign up form"""
        self.clear_window()
        self.root.configure(bg=BG_PRIMARY)
        
        # Header Badge
        header = tk.Label(
            self.root,
            text="VOTER REGISTRATION REGISTRY",
            font=("Helvetica", 14, "bold"),
            bg=COLOR_TEAL,
            fg=BG_PRIMARY,
            pady=12
        )
        header.pack(fill=tk.X, padx=0, pady=0)
        
        # Main frame with scrollbar
        main_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(15, 10))
        
        canvas = tk.Canvas(main_frame, bg=BG_PRIMARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style="TScrollbar")
        scrollable_frame = tk.Frame(canvas, bg=BG_PRIMARY)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=790)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Set Grid Weights for equal double column stretching
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        # Grid Field Mapping (Two Columns)
        fields_layout = [
            ("Aadhaar Number (12 digits)", "aadhaar", 0, 0),
            ("Gender (M/F/Other)", "gender", 0, 1),
            ("First Name", "fname", 1, 0),
            ("Middle Name (Optional)", "mname", 1, 1),
            ("Last Name", "lname", 2, 0),
            ("Date of Birth (YYYY-MM-DD)", "dob", 2, 1),
            ("Phone Number (10 digits)", "phone", 3, 0),
            ("Email Address", "email", 3, 1),
            ("Locality", "locality", 4, 0),
            ("City", "city", 4, 1),
            ("State", "state", 5, 0),
            ("Zip Code", "zip", 5, 1),
            ("Password", "password", 6, 0),
            ("Confirm Password", "confirm_pass", 6, 1)
        ]
        
        entries = {}
        for label_text, field_name, row, col in fields_layout:
            cell = tk.Frame(scrollable_frame, bg=BG_PRIMARY)
            cell.grid(row=row, column=col, padx=15, pady=8, sticky="ew")
            
            label = tk.Label(
                cell,
                text=label_text + ":",
                font=("Helvetica", 9, "bold"),
                bg=BG_PRIMARY,
                fg=COLOR_MUTED
            )
            label.pack(anchor=tk.W, pady=(0, 4))
            
            if "Password" in label_text:
                entry = tk.Entry(
                    cell, 
                    show="*", 
                    font=("Helvetica", 10),
                    bg=BG_INPUT,
                    fg="white",
                    insertbackground="white",
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground="#2b2654",
                    highlightcolor=COLOR_INDIGO
                )
            elif "Gender" in label_text:
                entry = ttk.Combobox(
                    cell, 
                    values=["M", "F", "Other"], 
                    font=("Helvetica", 10),
                    style="TCombobox"
                )
            else:
                entry = tk.Entry(
                    cell, 
                    font=("Helvetica", 10),
                    bg=BG_INPUT,
                    fg="white",
                    insertbackground="white",
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground="#2b2654",
                    highlightcolor=COLOR_INDIGO
                )
            
            entry.pack(fill=tk.X, ipady=4)
            entries[field_name] = entry
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        button_frame.pack(fill=tk.X, padx=35, pady=(5, 15))
        
        def register():
            try:
                aadhaar = entries["aadhaar"].get().strip()
                fname = entries["fname"].get().strip().upper()
                mname = entries["mname"].get().strip().upper()
                lname = entries["lname"].get().strip().upper()
                gender = entries["gender"].get().upper()
                dob = entries["dob"].get().strip()
                phone = entries["phone"].get().strip()
                email = entries["email"].get().strip().lower()
                locality = entries["locality"].get().strip().upper()
                city = entries["city"].get().strip().upper()
                state = entries["state"].get().strip().upper()
                password = entries["password"].get()
                confirm_pass = entries["confirm_pass"].get()
                
                # Validations
                if len(aadhaar) != 12 or not aadhaar.isnumeric():
                    messagebox.showerror("Invalid Input", "Aadhaar must be exactly 12 digits")
                    return
                
                if not fname.isalpha() or not lname.isalpha() or (mname and not mname.isalpha()):
                    messagebox.showerror("Invalid Input", "Names can only contain letters")
                    return
                
                if gender not in ["M", "F", "OTHER"]:
                    messagebox.showerror("Invalid Input", "Gender must be M, F, or Other")
                    return
                
                if len(phone) != 10 or not phone.isnumeric():
                    messagebox.showerror("Invalid Input", "Phone number must be exactly 10 digits")
                    return
                
                if '@' not in email or '.' not in email:
                    messagebox.showerror("Invalid Input", "Invalid email format")
                    return
                
                if password != confirm_pass:
                    messagebox.showerror("Mismatch", "Passwords do not match")
                    return
                
                if len(password) < 8:
                    messagebox.showerror("Invalid Input", "Password must be at least 8 characters long")
                    return
                
                # Date validation
                try:
                    datetime.datetime.strptime(dob, "%Y-%m-%d")
                    year = int(dob.split("-")[0])
                    age = date.today().year - year - 1
                    if age < 18:
                        messagebox.showerror("Age Restriction", "You must be at least 18 years old to vote")
                        return
                except ValueError:
                    messagebox.showerror("Invalid Date", "Date format must be YYYY-MM-DD")
                    return
                
                # Get district ID (parameterized)
                cur = self.db.cursor()
                cur.execute("SELECT DistrictId FROM address WHERE Locality = %s AND City = %s AND State = %s", (locality, city, state))
                result = cur.fetchone()
                if not result:
                    messagebox.showerror("Invalid Address", "District not found for this address. Verify Locality, City, State matches the registry.")
                    cur.close()
                    return
                
                district_id = result[0]
                
                # Check if already registered (parameterized)
                cur.execute("SELECT Aadhaar FROM voter_table WHERE Aadhaar = %s", (aadhaar,))
                if cur.fetchone():
                    messagebox.showerror("Already Registered", "This Aadhaar is already registered in the registry!")
                    cur.close()
                    return
                
                # Insert voter (parameterized)
                query = "INSERT INTO voter_table VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(query, (aadhaar, fname, mname, lname, gender, dob, age, int(phone), email, district_id))
                self.db.commit()
                
                # Create voter ID and insert user record with hashed password (parameterized)
                vid = fname[:2].upper() + lname[0].upper() + str(random.randint(1000001, 9999999))
                hashed_pwd = hash_password(password)
                
                query = "INSERT INTO user_table(VoterId, Aadhaar, _Password, IsActive) VALUES(%s, %s, %s, %s)"
                cur.execute(query, (vid, aadhaar, hashed_pwd, True))
                self.db.commit()
                cur.close()
                
                messagebox.showinfo("Success", f"Registration completed successfully!\nYour Voter ID: {vid}\nSave this code for your reference!")
                self.show_main_menu()
            
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")
        
        tk.Button(
            button_frame,
            text="Register Now",
            font=("Helvetica", 11, "bold"),
            bg=COLOR_TEAL,
            fg=BG_PRIMARY,
            command=register,
            width=20,
            relief="flat",
            activebackground=COLOR_TEAL_HOVER,
            activeforeground=BG_PRIMARY
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="Cancel & Back",
            font=("Helvetica", 11, "bold"),
            bg=BG_INPUT,
            fg=COLOR_TEXT,
            command=self.show_main_menu,
            width=20,
            relief="flat",
            activebackground="#2c3e50",
            activeforeground="white"
        ).pack(side=tk.LEFT, padx=10)
    
    def show_login(self):
        """Display login form"""
        self.clear_window()
        self.root.configure(bg=BG_PRIMARY)
        
        # Header
        header = tk.Label(
            self.root,
            text="VOTER DASHBOARD PORTAL",
            font=("Helvetica", 14, "bold"),
            bg=COLOR_INDIGO,
            fg='white',
            pady=12
        )
        header.pack(fill=tk.X, padx=0, pady=0)
        
        # Panel Frame
        frame = tk.Frame(self.root, bg=BG_SECONDARY, highlightthickness=1, highlightbackground='#17123a')
        frame.pack(expand=True, fill=tk.BOTH, padx=80, pady=50)
        
        # Login fields
        tk.Label(
            frame, 
            text="Aadhaar Number (12 digits):", 
            font=("Helvetica", 10, "bold"), 
            bg=BG_SECONDARY,
            fg=COLOR_MUTED
        ).pack(anchor=tk.W, padx=30, pady=(40, 5))
        
        aadhaar = tk.Entry(
            frame, 
            font=("Helvetica", 11),
            bg=BG_INPUT,
            fg="white",
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2b2654",
            highlightcolor=COLOR_INDIGO
        )
        aadhaar.pack(fill=tk.X, padx=30, ipady=5)
        
        tk.Label(
            frame, 
            text="Secure Password:", 
            font=("Helvetica", 10, "bold"), 
            bg=BG_SECONDARY,
            fg=COLOR_MUTED
        ).pack(anchor=tk.W, padx=30, pady=(20, 5))
        
        password = tk.Entry(
            frame, 
            show="*", 
            font=("Helvetica", 11),
            bg=BG_INPUT,
            fg="white",
            insertbackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#2b2654",
            highlightcolor=COLOR_INDIGO
        )
        password.pack(fill=tk.X, padx=30, ipady=5)
        
        def login():
            try:
                aadh = aadhaar.get().strip()
                pwd = password.get()
                
                cur = self.db.cursor()
                cur.execute("SELECT _Password, IsActive FROM user_table WHERE Aadhaar = %s", (aadh,))
                result = cur.fetchone()
                
                if result:
                    stored_pwd, is_active = result
                    if is_active is not None and not is_active:
                        messagebox.showerror("Inactive Account", "Your voter record is Inactive (Marked Deceased/Inactive)")
                        cur.close()
                        return
                    
                    if verify_password(stored_pwd, pwd):
                        self.current_user = aadh
                        cur.close()
                        messagebox.showinfo("Success", "Authenticated successfully! Accessing voter dashboard.")
                        self.show_after_login()
                        return
                
                cur.close()
                messagebox.showerror("Authentication Failed", "Invalid Aadhaar or Password credentials entered")
            
            except Exception as e:
                messagebox.showerror("Error", f"Login failed: {str(e)}")
        
        # Buttons
        button_frame = tk.Frame(frame, bg=BG_SECONDARY)
        button_frame.pack(fill=tk.X, padx=30, pady=30)
        
        tk.Button(
            button_frame,
            text="Secure Sign In",
            font=("Helvetica", 11, "bold"),
            bg=COLOR_INDIGO,
            fg='white',
            command=login,
            width=18,
            relief="flat",
            activebackground=COLOR_INDIGO_HOVER,
            activeforeground="white"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="Back to Menu",
            font=("Helvetica", 11, "bold"),
            bg=BG_INPUT,
            fg=COLOR_TEXT,
            command=self.show_main_menu,
            width=18,
            relief="flat",
            activebackground="#2b2654",
            activeforeground="white"
        ).pack(side=tk.LEFT)
    
    def show_after_login(self):
        """Display after login options"""
        self.clear_window()
        
        # Header
        header = tk.Label(
            self.root,
            text=f"WELCOME (Aadhaar: {self.current_user})",
            font=("Helvetica", 14, "bold"),
            bg='#9b59b6',
            fg='white'
        )
        header.pack(fill=tk.X, padx=0, pady=10)
        
        # Button frame
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        buttons = [
            ("🗳️ VOTE", self.show_vote),
            ("📝 UPDATE PROFILE", self.show_update_profile),
            ("📊 VIEW RESULTS", self.show_results),
            ("🔙 LOGOUT", self.show_main_menu)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                frame,
                text=text,
                font=("Helvetica", 12, "bold"),
                bg='#9b59b6',
                fg='white',
                command=command,
                height=3,
                cursor="hand2"
            )
            btn.pack(fill=tk.X, pady=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#8e44ad'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#9b59b6'))
    
    def show_vote(self):
        """Display voting interface"""
        self.clear_window()
        
        header = tk.Label(
            self.root,
            text="CAST YOUR VOTE",
            font=("Helvetica", 16, "bold"),
            bg='#e74c3c',
            fg='white'
        )
        header.pack(fill=tk.X, padx=0, pady=10)
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        try:
            cur = self.db.cursor()
            
            # Check if already voted (parameterized)
            cur.execute("SELECT VoteId FROM vote_table WHERE Aadhaar = %s", (self.current_user,))
            if cur.fetchone():
                cur.close()
                messagebox.showinfo("Already Voted", "You have already cast your vote!")
                self.show_after_login()
                return
            
            # Get district (parameterized)
            cur.execute("SELECT DistrictId FROM voter_table WHERE Aadhaar = %s", (self.current_user,))
            district = cur.fetchone()[0]
            
            # Get candidates (parameterized)
            cur.execute("SELECT pt.PartyName, ct.CandidateName, pt.PartyId, ct.CandidateId FROM party_table pt JOIN candidate_table ct ON pt.PartyId = ct.PartyId WHERE ct.DistrictId = %s", (district,))
            candidates = cur.fetchall()
            
            if not candidates:
                cur.close()
                messagebox.showinfo("No Candidates", "No candidates available in your district!")
                self.show_after_login()
                return
            
            # Display candidates
            tk.Label(frame, text="Available Candidates:", font=("Helvetica", 12, "bold"), bg='#f0f0f0').pack(anchor=tk.W, pady=10)
            
            selected_vote = tk.StringVar()
            
            for party, candidate, party_id, candidate_id in candidates:
                rb = tk.Radiobutton(
                    frame,
                    text=f"{party} - {candidate}",
                    variable=selected_vote,
                    value=f"{party_id}|{candidate_id}|{district}",
                    font=("Helvetica", 11),
                    bg='#f0f0f0'
                )
                rb.pack(anchor=tk.W, pady=8)
            
            def cast_vote():
                if not selected_vote.get():
                    messagebox.showwarning("No Selection", "Please select a candidate")
                    return
                
                try:
                    p_id, c_id, dist = selected_vote.get().split('|')
                    # Cast vote (parameterized)
                    query = "INSERT INTO vote_table(Aadhaar, PartyId, CandidateId, DistrictId) VALUES(%s, %s, %s, %s)"
                    cur.execute(query, (self.current_user, int(p_id), int(c_id), int(dist)))
                    self.db.commit()
                    cur.close()
                    
                    messagebox.showinfo("Success", "Thank you for voting!")
                    self.show_after_login()
                except Exception as e:
                    messagebox.showerror("Error", f"Voting failed: {str(e)}")
            
            button_frame = tk.Frame(frame, bg='#f0f0f0')
            button_frame.pack(fill=tk.X, pady=20)
            
            tk.Button(
                button_frame,
                text="Cast Vote",
                font=("Helvetica", 11, "bold"),
                bg='#e74c3c',
                fg='white',
                command=cast_vote,
                width=15
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                button_frame,
                text="Back",
                font=("Helvetica", 11, "bold"),
                bg='#95a5a6',
                fg='white',
                command=self.show_after_login,
                width=15
            ).pack(side=tk.LEFT, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error loading candidates: {str(e)}")
            self.show_after_login()
    
    def show_update_profile(self):
        """Display profile update form"""
        self.clear_window()
        
        header = tk.Label(
            self.root,
            text="UPDATE PROFILE",
            font=("Helvetica", 16, "bold"),
            bg='#f39c12',
            fg='white'
        )
        header.pack(fill=tk.X, padx=0, pady=10)
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        tk.Label(frame, text="What to Update:", font=("Helvetica", 11), bg='#f0f0f0').pack(anchor=tk.W, pady=10)
        update_option = ttk.Combobox(frame, values=["Name", "Phone", "Email"], font=("Helvetica", 11), state="readonly")
        update_option.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text="New Value:", font=("Helvetica", 11), bg='#f0f0f0').pack(anchor=tk.W, pady=10)
        value_entry = tk.Entry(frame, font=("Helvetica", 11))
        value_entry.pack(fill=tk.X, pady=5)
        
        def update():
            try:
                option = update_option.get()
                value = value_entry.get().strip()
                
                if not option or not value:
                    messagebox.showwarning("Empty Fields", "Please fill all fields")
                    return
                
                cur = self.db.cursor()
                
                if option == "Name":
                    parts = value.split()
                    if len(parts) < 2:
                        messagebox.showerror("Invalid Input", "Please enter at least First and Last name")
                        cur.close()
                        return
                    if len(parts) == 2:
                        first, middle, last = parts[0], "", parts[1]
                    else:
                        first, middle, last = parts[0], parts[1], " ".join(parts[2:])
                    query = "UPDATE voter_table SET FirstName = %s, MiddleName = %s, LastName = %s WHERE Aadhaar = %s"
                    params = (first.upper(), middle.upper(), last.upper(), self.current_user)
                
                elif option == "Phone":
                    if len(value) != 10 or not value.isnumeric():
                        messagebox.showerror("Invalid Input", "Phone must be 10 digits")
                        cur.close()
                        return
                    query = "UPDATE voter_table SET Phone = %s WHERE Aadhaar = %s"
                    params = (int(value), self.current_user)
                
                elif option == "Email":
                    if '@' not in value or '.' not in value:
                        messagebox.showerror("Invalid Input", "Invalid email format")
                        cur.close()
                        return
                    query = "UPDATE voter_table SET Email = %s WHERE Aadhaar = %s"
                    params = (value.lower(), self.current_user)
                else:
                    cur.close()
                    return
                
                cur.execute(query, params)
                self.db.commit()
                cur.close()
                messagebox.showinfo("Success", f"{option} updated successfully!")
                self.show_after_login()
            
            except Exception as e:
                messagebox.showerror("Error", f"Update failed: {str(e)}")
        
        button_frame = tk.Frame(frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(
            button_frame,
            text="Update",
            font=("Helvetica", 11, "bold"),
            bg='#f39c12',
            fg='white',
            command=update,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 11, "bold"),
            bg='#95a5a6',
            fg='white',
            command=self.show_after_login,
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def show_results(self):
        """Display voting results"""
        self.clear_window()
        
        header = tk.Label(
            self.root,
            text="VOTING RESULTS",
            font=("Helvetica", 16, "bold"),
            bg='#16a085',
            fg='white'
        )
        header.pack(fill=tk.X, padx=0, pady=10)
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        try:
            cur = self.db.cursor()
            cur.execute("SELECT pt.PartyId, pt.PartyName, COALESCE(SUM(r.Vote_Count), 0) as Total FROM party_table pt LEFT JOIN result r ON pt.PartyId = r.PartyId GROUP BY pt.PartyId, pt.PartyName ORDER BY Total DESC")
            results = cur.fetchall()
            cur.close()
            
            if not results:
                tk.Label(frame, text="No voting data available yet", font=("Helvetica", 12), bg='#f0f0f0').pack(pady=20)
            else:
                # Header
                header_frame = tk.Frame(frame, bg='#ecf0f1')
                header_frame.pack(fill=tk.X, padx=10, pady=10)
                
                tk.Label(header_frame, text="Party ID", font=("Helvetica", 11, "bold"), bg='#ecf0f1', width=10).pack(side=tk.LEFT, padx=5)
                tk.Label(header_frame, text="Party Name", font=("Helvetica", 11, "bold"), bg='#ecf0f1', width=20).pack(side=tk.LEFT, padx=5)
                tk.Label(header_frame, text="Total Votes", font=("Helvetica", 11, "bold"), bg='#ecf0f1', width=15).pack(side=tk.LEFT, padx=5)
                
                # Results
                for party_id, party_name, votes in results:
                    result_frame = tk.Frame(frame, bg='white', relief=tk.RAISED, bd=1)
                    result_frame.pack(fill=tk.X, padx=10, pady=5)
                    
                    tk.Label(result_frame, text=str(party_id), font=("Helvetica", 10), bg='white', width=10).pack(side=tk.LEFT, padx=5, pady=10)
                    tk.Label(result_frame, text=party_name, font=("Helvetica", 10), bg='white', width=20).pack(side=tk.LEFT, padx=5, pady=10)
                    tk.Label(result_frame, text=str(int(votes)), font=("Helvetica", 10, "bold"), bg='white', fg='#16a085', width=15).pack(side=tk.LEFT, padx=5, pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error loading results: {str(e)}")
        
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 11, "bold"),
            bg='#95a5a6',
            fg='white',
            command=self.show_main_menu if not self.current_user else self.show_after_login,
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def show_party_registration(self):
        """Display party registration form"""
        self.clear_window()
        
        header = tk.Label(
            self.root,
            text="PARTY REGISTRATION",
            font=("Helvetica", 16, "bold"),
            bg='#d35400',
            fg='white'
        )
        header.pack(fill=tk.X, padx=0, pady=10)
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        tk.Label(frame, text="Party Name:", font=("Helvetica", 11), bg='#f0f0f0').pack(anchor=tk.W, pady=5)
        party_name = tk.Entry(frame, font=("Helvetica", 11))
        party_name.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text="Party Symbol:", font=("Helvetica", 11), bg='#f0f0f0').pack(anchor=tk.W, pady=5)
        symbol = tk.Entry(frame, font=("Helvetica", 11))
        symbol.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text="Party Leader Name:", font=("Helvetica", 11), bg='#f0f0f0').pack(anchor=tk.W, pady=5)
        leader = tk.Entry(frame, font=("Helvetica", 11))
        leader.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text="Leader Aadhaar Number:", font=("Helvetica", 11), bg='#f0f0f0').pack(anchor=tk.W, pady=5)
        leader_aadhaar = tk.Entry(frame, font=("Helvetica", 11))
        leader_aadhaar.pack(fill=tk.X, pady=5)
        
        def register_party():
            try:
                pname = party_name.get().strip().upper()
                psymbol = symbol.get().strip().upper()
                pleader = leader.get().strip().upper()
                paadhaar = leader_aadhaar.get().strip()
                
                if not all([pname, psymbol, pleader, paadhaar]):
                    messagebox.showwarning("Empty Fields", "Please fill all fields")
                    return
                
                if len(paadhaar) != 12 or not paadhaar.isnumeric():
                    messagebox.showerror("Invalid", "Aadhaar must be 12 digits")
                    return
                
                cur = self.db.cursor()
                cur.execute(
                    "INSERT INTO party_table(PartyName, Symbol, PartyLeader, LeaderAadhaar) VALUES(%s, %s, %s, %s)",
                    (pname, psymbol, pleader, paadhaar)
                )
                self.db.commit()
                cur.close()
                
                messagebox.showinfo("Success", "Party registered successfully!")
                self.show_main_menu()
            
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")
        
        button_frame = tk.Frame(frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(
            button_frame,
            text="Register Party",
            font=("Helvetica", 11, "bold"),
            bg='#d35400',
            fg='white',
            command=register_party,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 11, "bold"),
            bg='#95a5a6',
            fg='white',
            command=self.show_main_menu,
            width=15
        ).pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = VotingSystemGUI(root)
    root.mainloop()
