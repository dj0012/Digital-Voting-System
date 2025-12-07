import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector as connector
from datetime import date
import random
import datetime


class VotingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Digital Voting Platform")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Database connection
        try:
            self.db = connector.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='root123',
                database='voting_system'
            )
        except Exception as e:
            messagebox.showerror("Database Error", f"Connection failed: {str(e)}")
            self.root.destroy()
            return
        
        self.current_user = None
        self.show_main_menu()
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Display the main menu"""
        self.clear_window()
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="SECURE DIGITAL VOTING PLATFORM",
            font=("Helvetica", 20, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        buttons = [
            ("🔐 SIGN UP", self.show_signup),
            ("📝 LOGIN", self.show_login),
            ("🎯 PARTY REGISTRATION", self.show_party_registration),
            ("📊 VIEW RESULTS", self.show_results),
            ("❌ EXIT", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Helvetica", 12, "bold"),
                bg='#3498db',
                fg='white',
                command=command,
                height=3,
                cursor="hand2"
            )
            btn.pack(fill=tk.X, pady=10)
            btn.bind("<Enter>", lambda e: btn.config(bg='#2980b9'))
            btn.bind("<Leave>", lambda e: btn.config(bg='#3498db'))
    
    def show_signup(self):
        """Display sign up form"""
        self.clear_window()
        
        # Header
        header = tk.Label(
            self.root,
            text="VOTER REGISTRATION",
            font=("Helvetica", 16, "bold"),
            bg='#27ae60',
            fg='white'
        )
        header.pack(fill=tk.X, padx=0, pady=10)
        
        # Main frame with scrollbar
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(main_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        fields = {
            "Aadhaar Number (12 digits)": "aadhaar",
            "First Name": "fname",
            "Middle Name": "mname",
            "Last Name": "lname",
            "Gender (M/F/Other)": "gender",
            "Date of Birth (YYYY-MM-DD)": "dob",
            "Phone Number (10 digits)": "phone",
            "Email Address": "email",
            "Locality": "locality",
            "City": "city",
            "State": "state",
            "Zip Code": "zip",
            "Password": "password",
            "Confirm Password": "confirm_pass"
        }
        
        entries = {}
        for label_text, field_name in fields.items():
            label = tk.Label(
                scrollable_frame,
                text=label_text + ":",
                font=("Helvetica", 10),
                bg='#f0f0f0',
                fg='#2c3e50'
            )
            label.pack(anchor=tk.W, pady=5)
            
            if "Password" in label_text:
                entry = tk.Entry(scrollable_frame, show="*", font=("Helvetica", 10))
            elif "Gender" in label_text:
                entry = ttk.Combobox(scrollable_frame, values=["M", "F", "Other"], font=("Helvetica", 10))
            else:
                entry = tk.Entry(scrollable_frame, font=("Helvetica", 10))
            
            entry.pack(fill=tk.X, pady=5)
            entries[field_name] = entry
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
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
                    messagebox.showerror("Invalid Input", "Aadhaar must be 12 digits")
                    return
                
                if not (fname.isalpha() and mname.isalpha() and lname.isalpha()):
                    messagebox.showerror("Invalid Input", "Names can only contain letters")
                    return
                
                if gender not in ["M", "F", "OTHER"]:
                    messagebox.showerror("Invalid Input", "Gender must be M, F, or Other")
                    return
                
                if len(phone) != 10 or not phone.isnumeric():
                    messagebox.showerror("Invalid Input", "Phone number must be 10 digits")
                    return
                
                if '@' not in email or '.' not in email:
                    messagebox.showerror("Invalid Input", "Invalid email format")
                    return
                
                if password != confirm_pass:
                    messagebox.showerror("Mismatch", "Passwords don't match")
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
                
                # Get district ID
                cur = self.db.cursor()
                cur.execute(f"SELECT DistrictId FROM address WHERE Locality='{locality}' AND City='{city}' AND State='{state}'")
                result = cur.fetchone()
                if not result:
                    messagebox.showerror("Invalid Address", "District not found for this address")
                    return
                
                district_id = result[0]
                
                # Check if already registered
                cur.execute(f"SELECT Aadhaar FROM voter_table WHERE Aadhaar='{aadhaar}'")
                if cur.fetchone():
                    messagebox.showerror("Already Registered", "You are already registered!")
                    return
                
                # Insert voter
                query = f"INSERT INTO voter_table VALUES('{aadhaar}','{fname}','{mname}','{lname}','{gender}','{dob}',{age},{phone},'{email}',{district_id})"
                cur.execute(query)
                self.db.commit()
                
                # Create voter ID
                vid = fname[:2].upper() + lname[0].upper() + str(random.randint(1000001, 9999999))
                query = f"INSERT INTO user_table VALUES('{vid}','{aadhaar}','{password}')"
                cur.execute(query)
                self.db.commit()
                
                messagebox.showinfo("Success", f"Registration completed!\nYour Voter ID: {vid}\nSave this for login!")
                self.show_main_menu()
            
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")
        
        tk.Button(
            button_frame,
            text="Register",
            font=("Helvetica", 11, "bold"),
            bg='#27ae60',
            fg='white',
            command=register,
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
    
    def show_login(self):
        """Display login form"""
        self.clear_window()
        
        # Header
        header = tk.Label(
            self.root,
            text="LOGIN",
            font=("Helvetica", 16, "bold"),
            bg='#3498db',
            fg='white'
        )
        header.pack(fill=tk.X, padx=0, pady=10)
        
        # Frame
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        # Login fields
        tk.Label(frame, text="Voter ID:", font=("Helvetica", 11), bg='#f0f0f0').pack(anchor=tk.W, pady=10)
        voter_id = tk.Entry(frame, font=("Helvetica", 11))
        voter_id.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text="Aadhaar Number:", font=("Helvetica", 11), bg='#f0f0f0').pack(anchor=tk.W, pady=10)
        aadhaar = tk.Entry(frame, font=("Helvetica", 11))
        aadhaar.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text="Password:", font=("Helvetica", 11), bg='#f0f0f0').pack(anchor=tk.W, pady=10)
        password = tk.Entry(frame, show="*", font=("Helvetica", 11))
        password.pack(fill=tk.X, pady=5)
        
        def login():
            try:
                vid = voter_id.get().strip()
                aadh = aadhaar.get().strip()
                pwd = password.get()
                
                cur = self.db.cursor()
                cur.execute(f"SELECT _Password FROM user_table WHERE VoterId='{vid}' AND Aadhaar='{aadh}'")
                result = cur.fetchone()
                
                if result and result[0] == pwd:
                    self.current_user = aadh
                    messagebox.showinfo("Success", "Login successful!")
                    self.show_after_login()
                else:
                    messagebox.showerror("Failed", "Invalid credentials")
            
            except Exception as e:
                messagebox.showerror("Error", f"Login failed: {str(e)}")
        
        # Buttons
        button_frame = tk.Frame(frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(
            button_frame,
            text="Login",
            font=("Helvetica", 11, "bold"),
            bg='#3498db',
            fg='white',
            command=login,
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
            
            # Check if already voted
            cur.execute(f"SELECT VoteId FROM vote_table WHERE Aadhaar='{self.current_user}'")
            if cur.fetchone():
                messagebox.showinfo("Already Voted", "You have already cast your vote!")
                self.show_after_login()
                return
            
            # Get district
            cur.execute(f"SELECT DistrictId FROM voter_table WHERE Aadhaar='{self.current_user}'")
            district = cur.fetchone()[0]
            
            # Get candidates
            cur.execute(f"SELECT PartyName, CandidateName, PartyId, CandidateId FROM party_table JOIN candidate_table ON party_table.PartyId = candidate_table.PartyId WHERE candidate_table.DistrictId={district}")
            candidates = cur.fetchall()
            
            if not candidates:
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
                    party_id, candidate_id, dist = selected_vote.get().split('|')
                    query = f"INSERT INTO vote_table(Aadhaar, PartyId, CandidateId, DistrictId) VALUES('{self.current_user}', {party_id}, {candidate_id}, {dist})"
                    cur.execute(query)
                    self.db.commit()
                    
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
                    if len(parts) < 3:
                        messagebox.showerror("Invalid Input", "Enter First Middle Last name")
                        return
                    query = f"UPDATE voter_table SET FirstName='{parts[0].upper()}', MiddleName='{parts[1].upper()}', LastName='{parts[2].upper()}' WHERE Aadhaar='{self.current_user}'"
                
                elif option == "Phone":
                    if len(value) != 10 or not value.isnumeric():
                        messagebox.showerror("Invalid Input", "Phone must be 10 digits")
                        return
                    query = f"UPDATE voter_table SET Phone={value} WHERE Aadhaar='{self.current_user}'"
                
                elif option == "Email":
                    if '@' not in value or '.' not in value:
                        messagebox.showerror("Invalid Input", "Invalid email format")
                        return
                    query = f"UPDATE voter_table SET Email='{value.lower()}' WHERE Aadhaar='{self.current_user}'"
                
                cur.execute(query)
                self.db.commit()
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
            cur.execute("SELECT party_table.PartyId, party_table.PartyName, COALESCE(SUM(result.Vote_Count), 0) as Total FROM party_table LEFT JOIN result ON party_table.PartyId = result.PartyId GROUP BY party_table.PartyId, party_table.PartyName ORDER BY Total DESC")
            results = cur.fetchall()
            
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
                cur.execute(f"INSERT INTO party_table(PartyName, Symbol, PartyLeader, LeaderAadhaar) VALUES('{pname}', '{psymbol}', '{pleader}', '{paadhaar}')")
                self.db.commit()
                
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
