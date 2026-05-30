import datetime
from datetime import date
import random
from db_utils import get_db_connection, hash_password, verify_password


class voting_system:
    def __init__(self):
        self.db = get_db_connection()
        
    def sign_up(self):
        while True:
            Aadhaar = input('Aadhaar number: ').strip()
            if len(Aadhaar) != 12:
                print("Invalid length of Aadhaar no.!\n")
            elif Aadhaar.isnumeric():
                break
            else:
                print("Aadhaar no. can only contain numbers!\n")
        
        cur = self.db.cursor()
        cur.execute("SELECT FirstName FROM voter_table WHERE Aadhaar = %s", (Aadhaar,))
        r = cur.fetchone()
        if r is not None:
            print("You are already registered!\n")
            cur.close()
            return
            
        while True:
            Fname = input("First Name: ").upper().strip()
            Mname = input("Middle Name: ").upper().strip()
            Lname = input("Last Name: ").upper().strip()
            if Fname.isalpha() and Lname.isalpha() and (not Mname or Mname.isalpha()):
                break
            else:
                print("Name can only contain characters!\n")
                
        while True:   
            Sex = input("Gender(F/M/Other): ").upper().strip()
            if Sex in ['F', 'M', 'OTHER']:
                break
            else:
                print("Please enter valid input!\n")
                
        while True:
            Birthday = input("Date of birth(YYYY-MM-DD): ").strip()
            format_str = "%Y-%m-%d"
            isValidDate = True
            try:
                datetime.datetime.strptime(Birthday, format_str)
            except ValueError:
                isValidDate = False
            if isValidDate:
                break
            else:
                print("This is the incorrect date string format. It should be YYYY-MM-DD\n")
                
        year, month, day = map(int, Birthday.split("-"))
        Age = date.today().year - year - 1
        if Age < 18:
            print("\nYou are not eligible to vote. Sorry!\n")
            print("Bye!")
            quit()
            
        while True:
            Phone = input("Phone Number: ").strip()
            if len(Phone) != 10:
                print("Invalid length of Phone no.!\n")
            elif Phone.isnumeric():
                Phone = int(Phone)
                break
            else:
                print("Phone no. can only contain numbers!\n")
                
        while True:        
            Email = input("Email address: ").strip()
            if ('@' in Email and '.' in Email) and (Email.index("@") < Email.index(".") and (Email.index(".") < len(Email) - 1)): 
                break
            else:
                print("Invalid Email Id !\n")
                
        print("\nEnter permanent address:")
        while True:
            locality = input("Locality: ").strip()
            city = input("City: ").strip()
            state = input("State: ").strip()
            zipCode = input("Zip Code: ").strip()
            DistrictId = self.districtId(locality, city, state)
            if DistrictId is None:
                print("Please enter valid address\n")
                continue
            break
            
        while True:
            Password = input("Password: ")
            Confirm_pass = input("Confirm password: ")
            if Confirm_pass == Password:
                break
            else:
                print("Password doesn't match! Enter again!\n")
        
        query = "INSERT INTO voter_table VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (Aadhaar, Fname, Mname, Lname, Sex, Birthday, Age, Phone, Email.lower(), DistrictId))
        self.db.commit()
        
        VoterId = self.user_table(Fname, Lname, Aadhaar, Password)
        cur.close()
        print("\nRegistration completed!\nPlease save the following voterId for future login\nVoterID: ", VoterId)
    
    def districtId(self, locality, city, state):
        query = "SELECT DistrictId FROM address WHERE Locality = %s AND City = %s AND State = %s"
        cur = self.db.cursor()
        cur.execute(query, (locality.upper(), city.upper(), state.upper()))
        distId = cur.fetchone()
        cur.close()
        if distId:
            return distId[0]
        return None
    
    def user_table(self, Fname, Lname, Aadhaar, Password):
        vid = Fname[:2].upper() + Lname[0].upper() + str(random.randint(1000001, 9999999))
        hashed_pwd = hash_password(Password)
        query = "INSERT INTO user_table(VoterId, Aadhaar, _Password, IsActive) VALUES(%s, %s, %s, %s)"
        cur = self.db.cursor()
        cur.execute(query, (vid, Aadhaar, hashed_pwd, True))
        self.db.commit()
        cur.close()
        return vid
    
    def login(self):
        while True:
            Aadhaar = input("Aadhaar Number: ").strip()
            Password = input("Password: ")
            
            query = "SELECT _Password, IsActive FROM user_table WHERE Aadhaar = %s"
            cur = self.db.cursor()
            cur.execute(query, (Aadhaar,))          
            result = cur.fetchone()
            cur.close()
            
            if result:
                stored_pwd, is_active = result
                # Support Task 3: Inactive voter filtering
                if is_active is not None and not is_active:
                    print("This voter record is Inactive (Marked Deceased/Inactive). Access denied.")
                elif verify_password(stored_pwd, Password):
                    print("Login successful!")
                    self.after_login(Aadhaar)            
                    break
                else:
                    print("Invalid password")
            else:
                print("Invalid credentials")
                
            leave = input("\nDo you want to leave?(YES/NO) ").strip().upper()
            if leave == "YES":
                print("Bye!!!")
                quit()
            print("\nPlease Try Again!\n")
    
    def after_login(self, Aadhaar):
        while True:
            query = "SELECT PartyLeader FROM party_table WHERE LeaderAadhaar = %s"
            cur = self.db.cursor()
            cur.execute(query, (Aadhaar,))
            r = cur.fetchone()
            cur.close()
            
            print("\n\nWhat do you want to do now?\n") 
            UserType = "Citizen"
            if r and r[0]:
                UserType = "Leader"
                
            if UserType == "Leader":
                process = input("Update personal details or party details or Vote: ").strip().upper()
            else:
                process = input("Update personal details or Vote: ").strip().upper()
                
            if process == "VOTE":
                cur = self.db.cursor()
                cur.execute("SELECT VoteId FROM vote_table WHERE Aadhaar = %s", (Aadhaar,))
                voted = cur.fetchone()
                cur.close()
                
                if voted:
                    print("\nYou have already submitted your vote!\n")
                    result = input("Do you want to see the current ranking?(YES/NO)\n ").strip().upper()
                    if result == "YES":
                        self.show_result()
                else:
                    self.vote(Aadhaar)
                
            elif process in ["PERSONAL DETAILS", "UPDATE PERSONAL DETAILS", "UPDATE"]:
                self.update(Aadhaar)
            elif UserType == "Leader" and process == "PARTY DETAILS":
                update = input("Add/Remove/View candidate/s or Edit party details: ").strip().upper()
                if update == "ADD":
                    self.add_candidate(Aadhaar)
                elif update == "REMOVE":
                    self.remove_candidate()
                elif update == "EDIT":
                    self.edit_party_details(Aadhaar)
                elif update == "VIEW":
                    self.party_candidate(Aadhaar)
            else:
                print("Invalid Input!")
                leave = input("Do you want to leave?(YES/NO) ").strip().upper()
                if leave == "YES":
                    print("Bye!")
                    quit()
    
    def vote(self, Aadhaar):
        cur = self.db.cursor()
        cur.execute("SELECT DistrictId FROM voter_table WHERE Aadhaar = %s", (Aadhaar,))          
        distId = cur.fetchone()
        if not distId:
            print("District error!")
            cur.close()
            return
        DistrictId = distId[0]
        
        # Get candidates (parameterized)
        query = "SELECT pt.PartyName, ct.CandidateName FROM party_table pt JOIN candidate_table ct ON pt.PartyId = ct.PartyId WHERE ct.DistrictId = %s"
        cur.execute(query, (DistrictId,))
        rows = cur.fetchall()
        
        if not rows:
            print("No candidates standing in your district!")
            cur.close()
            return
            
        print("Party Name\t Candidate Name")
        for row in rows:
            print(row[0], "\t ", row[1], "\n")
            
        v = input("Enter name of Party you are voting for: ").strip().upper()
        
        query = "SELECT pt.PartyId, ct.CandidateId FROM party_table pt JOIN candidate_table ct ON pt.PartyId = ct.PartyId WHERE ct.DistrictId = %s AND pt.PartyName = %s"
        cur.execute(query, (DistrictId, v))
        r = cur.fetchone()
        
        if not r:
            print("Invalid party selected!")
            cur.close()
            return
            
        PartyId = r[0]
        CandidateId = r[1]
        
        query = "INSERT INTO vote_table(Aadhaar, PartyId, CandidateId, DistrictId) VALUES(%s, %s, %s, %s)"
        cur.execute(query, (Aadhaar, PartyId, CandidateId, DistrictId))
        self.db.commit()
        cur.close()
        
        print("\nTHANK YOU FOR VOTING :)\n")
        result = input("Do you want to see the current ranking?(YES/NO) ").strip().upper()
        if result == "YES":
            self.show_result()
        
    def party_registration(self):
        while True:
            PartyName = input("Party Name: ").upper().strip()
            if PartyName.replace(" ", "").isalpha():
                break
            else:
                print("Party Name can only contain characters!\n")
        while True:
            Symbol = input("Enter Party Symbol: ").upper().strip()
            if Symbol.replace(" ", "").isalpha():
                break
            else:
                print("Party Symbol can only contain characters!\n")
        while True:
            PartyLeader = input("Party Leader's Name: ").upper().strip()
            if PartyLeader.replace(" ", "").isalpha():
                break
            else:
                print("Party Leader can only contain characters!\n")
        while True:
            LeaderAadhaar = input("Enter party leader's aadhaar number: ").strip()
            if len(LeaderAadhaar) != 12:
                print("Invalid length of Leader's Aadhaar no.!\n")
            elif LeaderAadhaar.isnumeric():
                break
            else:
                print("Leader's Aadhaar no. can only contain numbers!\n")
        
        leader_register = input("Is leader already registered?(YES/NO) ").strip().upper()
        if leader_register == "NO":
            self.sign_up()
            print("\n\n")
        
        query = "INSERT INTO party_table(PartyName, Symbol, PartyLeader, LeaderAadhaar) VALUES(%s, %s, %s, %s)"
        cur = self.db.cursor()
        cur.execute(query, (PartyName, Symbol, PartyLeader, LeaderAadhaar))
        self.db.commit()
        cur.close()
        print("\nYour party has been registered!\n")
        
    def edit_party_details(self, Aadhaar):
        edit = input("What do you want to edit (Party Leader / Party Name / Party Symbol): ").strip().upper()
        cur = self.db.cursor()
        
        if edit == "PARTY LEADER":
            leader_register = input("Is leader already registered?(YES/NO) ").strip().upper()
            if leader_register == "NO":
                self.sign_up()
                print("\n\n")
            while True:
                NewName = input("Enter new leader's name: ").upper().strip()
                if NewName.replace(" ", "").isalpha():
                    break
                else:
                    print("Name can only contain characters!\n")
            while True:
                NewAadhaar = input("Enter new leader's Aadhaar: ").strip()
                if len(NewAadhaar) != 12:
                    print("Invalid length of Leader's Aadhaar no.!\n")
                elif NewAadhaar.isnumeric():
                    break
                else:
                    print("Leader's Aadhaar no. can only contain numbers!\n")
            query_1 = "UPDATE party_table SET PartyLeader = %s, LeaderAadhaar = %s WHERE LeaderAadhaar = %s"
            params = (NewName, NewAadhaar, Aadhaar)
            
        elif edit == "PARTY NAME":
            while True:
                NewPartyName = input("Enter new party name: ").upper().strip()
                if NewPartyName.replace(" ", "").isalpha():
                    break
                else:
                    print("Party Name can only contain characters!\n")
            query_1 = "UPDATE party_table SET PartyName = %s WHERE LeaderAadhaar = %s"
            params = (NewPartyName, Aadhaar)
            
        elif edit == "PARTY SYMBOL":
            while True:
                NewSymbol = input("Enter new symbol: ").upper().strip()
                if NewSymbol.replace(" ", "").isalpha():
                    break
                else:
                    print("Party Symbol can only contain characters!\n")
            query_1 = "UPDATE party_table SET Symbol = %s WHERE LeaderAadhaar = %s"
            params = (NewSymbol, Aadhaar)
        else:
            print("Invalid Option!")
            cur.close()
            return
            
        try:
            cur.execute(query_1, params)
            self.db.commit()
            print(f"\nYour '{edit}' has been changed\n")
        except Exception as e:
            print("Invalid Input or error:", e)
        finally:
            cur.close()
            
    def add_candidate(self, Aadhaar):
        cur = self.db.cursor()
        cur.execute("SELECT PartyId FROM party_table WHERE LeaderAadhaar = %s", (Aadhaar,))
        r = cur.fetchone()
        if not r:
            print("You are not registered as a party leader!")
            cur.close()
            return
        PartyId = r[0]
        
        candidate_register = input("Is candidate already registered?(YES/NO) ").strip().upper()
        if candidate_register == "NO":
            self.sign_up()
        
        while True:
            CandidateAadhaar = input("Enter candidate's aadhaar number: ").strip()
            if len(CandidateAadhaar) != 12:
                print("Invalid length of Candidate's Aadhaar no.!\n")
            elif CandidateAadhaar.isnumeric():
                break
            else:
                print("Candidate's Aadhaar no. can only contain numbers!\n")
                
        print("Enter address where candidate is standing for election:\n")
        while True:
            locality = input("Locality: ").strip()
            city = input("City: ").strip()
            state = input("State: ").strip()
            zipCode = input("Zip Code: ").strip()
            DistrictId = self.districtId(locality, city, state)
            if DistrictId is None:
                print("Please enter valid address\n")
                continue
            break
            
        cur.execute("SELECT FirstName, LastName FROM voter_table WHERE Aadhaar = %s", (CandidateAadhaar,))
        names = cur.fetchone()
        if not names:
            print("Candidate is not registered as a voter!")
            cur.close()
            return
            
        CandidateName = names[0] + " " + names[1]
        
        query = "INSERT INTO candidate_table(Aadhaar, CandidateName, PartyId, DistrictId) VALUES(%s, %s, %s, %s)"
        cur.execute(query, (CandidateAadhaar, CandidateName, PartyId, DistrictId))
        self.db.commit()
        cur.close()
        print("\nCandidate added successfully!\n") 
        
    def remove_candidate(self):
        while True:
            CandidateAadhaar = input("Enter candidate's aadhaar number: ").strip()
            if len(CandidateAadhaar) != 12:
                print("Invalid length of Candidate's Aadhaar no.!\n")
            elif CandidateAadhaar.isnumeric():
                break
            else:
                print("Candidate's Aadhaar no. can only contain numbers!\n")
                
        query = "DELETE FROM candidate_table WHERE Aadhaar = %s"
        cur = self.db.cursor()
        cur.execute(query, (CandidateAadhaar,))
        self.db.commit()
        cur.close()
        print("\nCandidate removed successfully!\n")
    
    def update(self, Aadhaar):
        inp = input("What do you want to update (Name / Phone / Email / Address): ").strip().upper()
        cur = self.db.cursor()
        
        if inp == "NAME":
            while True:
                first = input("Enter first name: ").upper().strip()
                middle = input("Enter middle name (Optional): ").upper().strip()
                last = input("Enter last name: ").upper().strip()
                if first.isalpha() and last.isalpha() and (not middle or middle.isalpha()):
                    break
                else:
                    print("Name can only contain characters!\n")
            query_2 = "UPDATE voter_table SET FirstName = %s, MiddleName = %s, LastName = %s WHERE Aadhaar = %s"
            params = (first, middle, last, Aadhaar)
           
        elif inp == "PHONE":
            while True:
                phone = input("Enter new phone number: ").strip()
                if len(phone) != 10:
                    print("Invalid length of Phone no.!\n")
                elif phone.isnumeric():
                    phone = int(phone)
                    break
                else:
                    print("Phone no. can only contain numbers!\n")
            query_2 = "UPDATE voter_table SET Phone = %s WHERE Aadhaar = %s"
            params = (phone, Aadhaar)
            
        elif inp == "EMAIL":
            while True:
                email = input("Enter new email id: ").strip()
                if ('@' in email and '.' in email) and (email.index("@") < email.index(".") and (email.index(".") < len(email) - 1)):
                    break
                else:
                    print("Invalid Email Id !\n")
            query_2 = "UPDATE voter_table SET Email = %s WHERE Aadhaar = %s"
            params = (email, Aadhaar)
            
        elif inp == "ADDRESS":
            while True:
                locality = input("Enter new locality: ").strip()
                city = input("Enter new city: ").strip()
                state = input("Enter new state: ").strip()
                zipcode = input("Enter new zipcode: ").strip()
                DistrictId = self.districtId(locality, city, state)
                if DistrictId is None:
                    print("Please enter valid address")
                    continue
                break
            query_2 = "UPDATE voter_table SET DistrictId = %s WHERE Aadhaar = %s"
            params = (DistrictId, Aadhaar)
        else:
            cur.close()
            return
            
        try:
            cur.execute(query_2, params)
            self.db.commit()
            print(f"\n Your '{inp}' has been updated\n")
            again = input("Do you want to update something else?(YES/NO): ").strip().upper()
            if again == "YES":
                self.update(Aadhaar)
        except Exception as e:
            print("Invalid Input or error:", e)
        finally:
            cur.close()
            
    def show_result(self):
        query = "SELECT pt.PartyId, pt.PartyName, COALESCE(SUM(r.Vote_Count), 0) AS Total_Count FROM party_table pt LEFT JOIN result r ON pt.PartyId = r.PartyId GROUP BY pt.PartyId, pt.PartyName ORDER BY Total_Count DESC"
        cur = self.db.cursor()
        cur.execute(query)
        print("\n\tVOTES FOR EACH PARTY\n")
        print("Party ID   Party Name   Count")
        for i in cur.fetchall():
            print("  ", i[0], "\t\t ", i[1], "\t  ", int(i[2]), '\n')
        cur.close()
            
    def party_candidate(self, Aadhaar):
        cur = self.db.cursor()
        cur.execute("SELECT PartyId, PartyName FROM party_table WHERE LeaderAadhaar = %s", (Aadhaar,))
        r = cur.fetchone()
        if not r:
            print("Not a leader!")
            cur.close()
            return
            
        PartyId = r[0]
        PartyName = r[1]
        print(f"\nShowing candidate details for '{PartyName}' party\n")
        
        query_2 = "SELECT vt.FirstName, vt.LastName, addr.Locality, addr.City, addr.State FROM voter_table vt JOIN candidate_table ct ON vt.Aadhaar = ct.Aadhaar JOIN address addr ON ct.DistrictId = addr.DistrictId WHERE ct.PartyId = %s"
        cur.execute(query_2, (PartyId,))
        rows = cur.fetchall()
        cur.close()
        
        print("\t{:<15} {:<15} {:<10} {:10}".format("Name", "Locality", "City", "State"))
        for r in rows:
            name = r[0] + " " + r[1]
            print("{:<15} \t{:<15} {:<10} {:<10}".format(name, r[2], r[3], r[4]))


if __name__ == "__main__":
    vs = voting_system()
    while True:
        print("What do you want to do?\n")
        print("SIGN UP\t LOGIN\t PARTY REGISTRATION\tVIEW RESULT\t LEAVE") 
        task = input("What do you want to do? ").strip().upper()
        if task == "SIGN UP":
            print("\n\n\nSIGN UP:\n")
            vs.sign_up()
        elif task == "PARTY REGISTRATION":
            print("\n\n\nPARTY REGISTRATION:\n")
            vs.party_registration()
        elif task == "LOGIN":
            print("\n\n\nLOGIN:\n")
            vs.login()
        elif task == "VIEW RESULT":
            vs.show_result()
        elif task == "LEAVE":
            print("\n\n\nBYE!!!")
            quit()
        else:
            print("Invalid Input!")
