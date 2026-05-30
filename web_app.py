import re
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import date, datetime, timedelta
import random
import os
from db_utils import get_db_connection, hash_password, verify_password

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'change-this-secret-key-for-production')
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=os.environ.get('SESSION_COOKIE_SECURE', 'false').strip().lower() in ('1', 'true', 'yes')
)

EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def calculate_age(dob_obj: date) -> int:
    today = date.today()
    age = today.year - dob_obj.year
    if (today.month, today.day) < (dob_obj.month, dob_obj.day):
        age -= 1
    return age


@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'same-origin'
    return response

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
            zip_code = data.get('zip', '').strip()
            password = data.get('password', '')
            confirm_pass = data.get('confirm_pass', '')
            
            # Validations
            if len(aadhaar) != 12 or not aadhaar.isnumeric():
                return jsonify({'success': False, 'message': 'Aadhaar must be 12 digits'}), 400
            
            if not fname.isalpha() or not lname.isalpha() or (mname and not mname.isalpha()):
                return jsonify({'success': False, 'message': 'Names can only contain letters'}), 400
            
            if gender not in ['M', 'F', 'OTHER']:
                return jsonify({'success': False, 'message': 'Invalid gender'}), 400
            
            if len(phone) != 10 or not phone.isnumeric():
                return jsonify({'success': False, 'message': 'Phone must be 10 digits'}), 400
            
            if not EMAIL_PATTERN.match(email):
                return jsonify({'success': False, 'message': 'Invalid email format'}), 400

            if not zip_code.isdigit() or not (3 <= len(zip_code) <= 10):
                return jsonify({'success': False, 'message': 'Zip code must be numeric and 3-10 digits'}), 400
            
            if password != confirm_pass:
                return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
            
            try:
                dob_obj = datetime.strptime(dob, "%Y-%m-%d")
                age = calculate_age(dob_obj)
                if age < 18:
                    return jsonify({'success': False, 'message': 'Must be 18 years old to vote'}), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid date format (use YYYY-MM-DD)'}), 400
            
            db = get_db_connection()
            cur = db.cursor()
            
            # Check if already registered
            cur.execute("SELECT Aadhaar FROM voter_table WHERE Aadhaar = %s", (aadhaar,))
            if cur.fetchone():
                cur.close()
                db.close()
                return jsonify({'success': False, 'message': 'Already registered!'}), 400
            
            # Get district ID
            cur.execute(
                "SELECT DistrictId FROM address WHERE Locality = %s AND City = %s AND State = %s AND Zip = %s",
                (locality, city, state, zip_code)
            )
            district_result = cur.fetchone()
            if not district_result:
                cur.close()
                db.close()
                return jsonify({'success': False, 'message': 'Invalid address'}), 400
            
            district_id = district_result[0]
            
            # Insert voter
            query = "INSERT INTO voter_table(Aadhaar, FirstName, MiddleName, LastName, Sex, Birthday, Age, Phone, Email, DistrictId) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (aadhaar, fname, mname, lname, gender, dob, age, int(phone), email, district_id))
            db.commit()
            
            # Create voter ID and insert with hashed password
            vid = fname[:2].upper() + lname[0].upper() + str(random.randint(1000001, 9999999))
            hashed_pass = hash_password(password)
            
            query = "INSERT INTO user_table(VoterId, Aadhaar, _Password, IsActive) VALUES(%s, %s, %s, %s)"
            cur.execute(query, (vid, aadhaar, hashed_pass, True))
            db.commit()
            
            cur.close()
            db.close()
            
            return jsonify({'success': True, 'message': f'Registration successful! Your Voter ID: {vid}', 'voter_id': vid}), 200
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            aadhaar = data.get('aadhaar', '').strip()
            password = data.get('password', '')
            
            db = get_db_connection()
            cur = db.cursor()
            
            cur.execute("SELECT _Password, IsActive FROM user_table WHERE Aadhaar = %s", (aadhaar,))
            result = cur.fetchone()
            
            if result:
                stored_password, is_active = result
                # Support Task 3: IsActive check to prevent deceased/inactive voters from voting
                if is_active is not None and not is_active:
                    cur.close()
                    db.close()
                    return jsonify({'success': False, 'message': 'Voter record is Inactive (Marked Deceased/Inactive)'}), 403
                
                if verify_password(stored_password, password):
                    session['user_aadhaar'] = aadhaar
                    cur.close()
                    db.close()
                    return jsonify({'success': True, 'message': 'Login successful!'}), 200
            
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
            try:
                party_id = int(data.get('party_id'))
                candidate_id = int(data.get('candidate_id'))
            except (TypeError, ValueError):
                return jsonify({'success': False, 'message': 'Invalid candidate or party selection'}), 400
            
            aadhaar = session['user_aadhaar']
            
            db = get_db_connection()
            cur = db.cursor()
            
            # Check if already voted
            cur.execute("SELECT VoteId FROM vote_table WHERE Aadhaar = %s", (aadhaar,))
            if cur.fetchone():
                cur.close()
                db.close()
                return jsonify({'success': False, 'message': 'Already voted'}), 400
            
            # Get district
            cur.execute("SELECT DistrictId FROM voter_table WHERE Aadhaar = %s", (aadhaar,))
            district = cur.fetchone()[0]

            cur.execute(
                "SELECT CandidateId FROM candidate_table WHERE CandidateId = %s AND PartyId = %s AND DistrictId = %s",
                (candidate_id, party_id, district)
            )
            candidate_match = cur.fetchone()
            if not candidate_match:
                cur.close()
                db.close()
                return jsonify({'success': False, 'message': 'Invalid candidate or party for your district'}), 400
            
            query = "INSERT INTO vote_table(Aadhaar, PartyId, CandidateId, DistrictId) VALUES(%s, %s, %s, %s)"
            cur.execute(query, (aadhaar, party_id, candidate_id, district))
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
        cur.execute("SELECT VoteId FROM vote_table WHERE Aadhaar = %s", (aadhaar,))
        if cur.fetchone():
            cur.close()
            db.close()
            return render_template('vote.html', already_voted=True, candidates=[])
        
        # Get district
        cur.execute("SELECT DistrictId FROM voter_table WHERE Aadhaar = %s", (aadhaar,))
        district = cur.fetchone()[0]
        
        # Get candidates
        cur.execute("SELECT pt.PartyId, pt.PartyName, ct.CandidateId, ct.CandidateName FROM party_table pt JOIN candidate_table ct ON pt.PartyId = ct.PartyId WHERE ct.DistrictId = %s", (district,))
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
        
        cur.execute(
            "SELECT pt.PartyId, pt.PartyName, COALESCE(COUNT(v.VoteId), 0) AS Total "
            "FROM party_table pt LEFT JOIN vote_table v ON pt.PartyId = v.PartyId "
            "GROUP BY pt.PartyId, pt.PartyName ORDER BY Total DESC"
        )
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
                if len(parts) < 2:
                    cur.close()
                    db.close()
                    return jsonify({'success': False, 'message': 'Please enter at least First and Last name'}), 400
                if len(parts) == 2:
                    first, middle, last = parts[0], "", parts[1]
                else:
                    first, middle, last = parts[0], parts[1], " ".join(parts[2:])
                query = "UPDATE voter_table SET FirstName = %s, MiddleName = %s, LastName = %s WHERE Aadhaar = %s"
                params = (first.upper(), middle.upper(), last.upper(), aadhaar)
            
            elif update_type == 'phone':
                if len(value) != 10 or not value.isnumeric():
                    cur.close()
                    db.close()
                    return jsonify({'success': False, 'message': 'Phone must be 10 digits'}), 400
                query = "UPDATE voter_table SET Phone = %s WHERE Aadhaar = %s"
                params = (int(value), aadhaar)
            
            elif update_type == 'email':
                if not EMAIL_PATTERN.match(value.lower()):
                    cur.close()
                    db.close()
                    return jsonify({'success': False, 'message': 'Invalid email format'}), 400
                query = "UPDATE voter_table SET Email = %s WHERE Aadhaar = %s"
                params = (value.lower(), aadhaar)
            else:
                cur.close()
                db.close()
                return jsonify({'success': False, 'message': 'Invalid update type'}), 400
            
            cur.execute(query, params)
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
        
        cur.execute("SELECT FirstName, MiddleName, LastName, Phone, Email, Birthday FROM voter_table WHERE Aadhaar = %s", (aadhaar,))
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
        
        cur.execute("SELECT DistrictId FROM voter_table WHERE Aadhaar = %s", (aadhaar,))
        district = cur.fetchone()[0]
        
        cur.execute("SELECT pt.PartyId, pt.PartyName, ct.CandidateId, ct.CandidateName FROM party_table pt JOIN candidate_table ct ON pt.PartyId = ct.PartyId WHERE ct.DistrictId = %s", (district,))
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
    app.run(debug=True, host='0.0.0.0', port=8080)
