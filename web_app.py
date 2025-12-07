from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector as connector
from datetime import date, datetime, timedelta
import random
import os

app = Flask(__name__)
app.secret_key = 'secure_voting_platform_secret_key_2024'

def get_db_connection():
    return connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root123',
        database='voting_system'
    )

@app.route('/')
def index():
    return redirect(url_for('main_menu'))

@app.route('/menu')
def main_menu():
    return render_template('menu.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            data = request.get_json()
            aadhaar = data.get('aadhaar', '').strip()
            fname = data.get('fname', '').strip().upper()
            mname = data.get('mname', '').strip().upper()
            lname = data.get('lname', '').strip().upper()
            gender = data.get('gender', '').upper()
            dob = data.get('dob', '').strip()
            phone = data.get('phone', '').strip()
            email = data.get('email', '').strip().lower()
            locality = data.get('locality', '').strip().upper()
            city = data.get('city', '').strip().upper()
            state = data.get('state', '').strip().upper()
            password = data.get('password', '')
            confirm_pass = data.get('confirm_pass', '')
            
            # Validations
            if len(aadhaar) != 12 or not aadhaar.isnumeric():
                return jsonify({'success': False, 'message': 'Aadhaar must be 12 digits'}), 400
            
            if not (fname.isalpha() and mname.isalpha() and lname.isalpha()):
                return jsonify({'success': False, 'message': 'Names can only contain letters'}), 400
            
            if gender not in ['M', 'F', 'OTHER']:
                return jsonify({'success': False, 'message': 'Invalid gender'}), 400
            
            if len(phone) != 10 or not phone.isnumeric():
                return jsonify({'success': False, 'message': 'Phone must be 10 digits'}), 400
            
            if '@' not in email or '.' not in email:
                return jsonify({'success': False, 'message': 'Invalid email format'}), 400
            
            if password != confirm_pass:
                return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
            
            try:
                dob_obj = datetime.strptime(dob, "%Y-%m-%d")
                age = date.today().year - dob_obj.year - 1
                if age < 18:
                    return jsonify({'success': False, 'message': 'Must be 18 years old to vote'}), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid date format (use YYYY-MM-DD)'}), 400
            
            db = get_db_connection()
            cur = db.cursor()
            
            # Check if already registered
            cur.execute(f"SELECT Aadhaar FROM voter_table WHERE Aadhaar='{aadhaar}'")
            if cur.fetchone():
                return jsonify({'success': False, 'message': 'Already registered!'}), 400
            
            # Get district ID
            cur.execute(f"SELECT DistrictId FROM address WHERE Locality='{locality}' AND City='{city}' AND State='{state}'")
            district_result = cur.fetchone()
            if not district_result:
                return jsonify({'success': False, 'message': 'Invalid address'}), 400
            
            district_id = district_result[0]
            
            # Insert voter
            query = f"INSERT INTO voter_table VALUES('{aadhaar}','{fname}','{mname}','{lname}','{gender}','{dob}',{age},{phone},'{email}',{district_id})"
            cur.execute(query)
            db.commit()
            
            # Create voter ID
            vid = fname[:2].upper() + lname[0].upper() + str(random.randint(1000001, 9999999))
            query = f"INSERT INTO user_table VALUES('{vid}','{aadhaar}','{password}')"
            cur.execute(query)
            db.commit()
            
            cur.close()
            db.close()
            
            return jsonify({'success': True, 'message': f'Registration successful! Your Voter ID: {vid}'}), 200
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            voter_id = data.get('voter_id', '').strip()
            aadhaar = data.get('aadhaar', '').strip()
            password = data.get('password', '')
            
            db = get_db_connection()
            cur = db.cursor()
            
            cur.execute(f"SELECT _Password FROM user_table WHERE VoterId='{voter_id}' AND Aadhaar='{aadhaar}'")
            result = cur.fetchone()
            
            if result and result[0] == password:
                session['user_aadhaar'] = aadhaar
                cur.close()
                db.close()
                return jsonify({'success': True, 'message': 'Login successful!'}), 200
            else:
                cur.close()
                db.close()
                return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_aadhaar' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', aadhaar=session['user_aadhaar'])

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'user_aadhaar' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            party_id = data.get('party_id')
            candidate_id = data.get('candidate_id')
            
            aadhaar = session['user_aadhaar']
            
            db = get_db_connection()
            cur = db.cursor()
            
            # Check if already voted
            cur.execute(f"SELECT VoteId FROM vote_table WHERE Aadhaar='{aadhaar}'")
            if cur.fetchone():
                cur.close()
                db.close()
                return jsonify({'success': False, 'message': 'Already voted'}), 400
            
            # Get district
            cur.execute(f"SELECT DistrictId FROM voter_table WHERE Aadhaar='{aadhaar}'")
            district = cur.fetchone()[0]
            
            # Insert vote
            query = f"INSERT INTO vote_table(Aadhaar, PartyId, CandidateId, DistrictId) VALUES('{aadhaar}', {party_id}, {candidate_id}, {district})"
            cur.execute(query)
            db.commit()
            
            cur.close()
            db.close()
            
            return jsonify({'success': True, 'message': 'Vote cast successfully!'}), 200
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    # GET request - get candidates for user's district
    try:
        aadhaar = session['user_aadhaar']
        db = get_db_connection()
        cur = db.cursor()
        
        # Check if already voted
        cur.execute(f"SELECT VoteId FROM vote_table WHERE Aadhaar='{aadhaar}'")
        if cur.fetchone():
            cur.close()
            db.close()
            return render_template('vote.html', already_voted=True, candidates=[])
        
        # Get district
        cur.execute(f"SELECT DistrictId FROM voter_table WHERE Aadhaar='{aadhaar}'")
        district = cur.fetchone()[0]
        
        # Get candidates
        cur.execute(f"SELECT pt.PartyId, pt.PartyName, ct.CandidateId, ct.CandidateName FROM party_table pt JOIN candidate_table ct ON pt.PartyId = ct.PartyId WHERE ct.DistrictId={district}")
        candidates = cur.fetchall()
        
        cur.close()
        db.close()
        
        return render_template('vote.html', already_voted=False, candidates=candidates)
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/results')
def results():
    try:
        db = get_db_connection()
        cur = db.cursor()
        
        cur.execute("SELECT pt.PartyId, pt.PartyName, COALESCE(SUM(r.Vote_Count), 0) as Total FROM party_table pt LEFT JOIN result r ON pt.PartyId = r.PartyId GROUP BY pt.PartyId, pt.PartyName ORDER BY Total DESC")
        results = cur.fetchall()
        
        cur.close()
        db.close()
        
        return render_template('results.html', results=results)
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_aadhaar' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            update_type = data.get('type')
            value = data.get('value', '').strip()
            aadhaar = session['user_aadhaar']
            
            db = get_db_connection()
            cur = db.cursor()
            
            if update_type == 'name':
                parts = value.split()
                if len(parts) < 3:
                    return jsonify({'success': False, 'message': 'Enter First Middle Last name'}), 400
                query = f"UPDATE voter_table SET FirstName='{parts[0].upper()}', MiddleName='{parts[1].upper()}', LastName='{parts[2].upper()}' WHERE Aadhaar='{aadhaar}'"
            
            elif update_type == 'phone':
                if len(value) != 10 or not value.isnumeric():
                    return jsonify({'success': False, 'message': 'Phone must be 10 digits'}), 400
                query = f"UPDATE voter_table SET Phone={value} WHERE Aadhaar='{aadhaar}'"
            
            elif update_type == 'email':
                if '@' not in value or '.' not in value:
                    return jsonify({'success': False, 'message': 'Invalid email format'}), 400
                query = f"UPDATE voter_table SET Email='{value.lower()}' WHERE Aadhaar='{aadhaar}'"
            
            cur.execute(query)
            db.commit()
            cur.close()
            db.close()
            
            return jsonify({'success': True, 'message': f'{update_type.capitalize()} updated successfully!'}), 200
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    try:
        aadhaar = session['user_aadhaar']
        db = get_db_connection()
        cur = db.cursor()
        
        cur.execute(f"SELECT FirstName, MiddleName, LastName, Phone, Email, Birthday FROM voter_table WHERE Aadhaar='{aadhaar}'")
        profile_data = cur.fetchone()
        
        cur.close()
        db.close()
        
        if profile_data:
            return render_template('profile.html', profile=profile_data)
        else:
            return redirect(url_for('login'))
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_menu'))

@app.route('/api/candidates')
def get_candidates():
    if 'user_aadhaar' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        aadhaar = session['user_aadhaar']
        db = get_db_connection()
        cur = db.cursor()
        
        cur.execute(f"SELECT DistrictId FROM voter_table WHERE Aadhaar='{aadhaar}'")
        district = cur.fetchone()[0]
        
        cur.execute(f"SELECT pt.PartyId, pt.PartyName, ct.CandidateId, ct.CandidateName FROM party_table pt JOIN candidate_table ct ON pt.PartyId = ct.PartyId WHERE ct.DistrictId={district}")
        candidates = cur.fetchall()
        
        cur.close()
        db.close()
        
        candidates_list = [
            {
                'party_id': c[0],
                'party_name': c[1],
                'candidate_id': c[2],
                'candidate_name': c[3]
            }
            for c in candidates
        ]
        
        return jsonify({'success': True, 'candidates': candidates_list}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
