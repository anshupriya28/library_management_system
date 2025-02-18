from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'library_secret'

# Constants
MAX_ISSUE_DAYS = 15
MEMBERSHIP_DURATIONS = {
    '6_months': 180,
    '1_year': 365,
    '2_years': 730
}

# Dummy users (Admin & User)
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user': {'password': 'user123', 'role': 'user'}
}

books = []
members = []
transactions = []
fines = []

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username]['password'] == password:
        session['username'] = username
        session['role'] = users[username]['role']
        return redirect(url_for('dashboard'))
    return render_template('login.html', error='Invalid Credentials')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html', role=session['role'])

# Maintenance Routes (Admin only)
@app.route('/maintenance')
def maintenance():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
    return render_template('maintenance.html')

@app.route('/system_settings', methods=['GET', 'POST'])
def system_settings():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
    # Implementation for system settings
    return render_template('system_settings.html')

# Reports Routes (Admin and User)
@app.route('/reports')
def reports():
    if 'username' not in session:
        return redirect(url_for('dashboard'))
    return render_template('reports.html')

@app.route('/book_report')
def book_report():
    if 'username' not in session:
        return redirect(url_for('dashboard'))
    return render_template('book_report.html', books=books)

@app.route('/transaction_report')
def transaction_report():
    if 'username' not in session:
        return redirect(url_for('dashboard'))
    return render_template('transaction_report.html', transactions=transactions)

# User Management Routes (Admin only)
@app.route('/user_management')
def user_management():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
    return render_template('user_management.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if username and password and role:
            users[username] = {'password': password, 'role': role}
            flash('User added successfully!', 'success')
            return redirect(url_for('user_management'))
        else:
            flash('Please fill all required fields', 'error')
    return render_template('add_user.html')

# Membership Management Routes
@app.route('/membership')
def membership():
    if 'username' not in session:
        return redirect(url_for('dashboard'))
    return render_template('membership.html', members=members)

@app.route('/add_membership', methods=['GET', 'POST'])
def add_membership():
    if 'username' not in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        member_name = request.form['member_name']
        duration = request.form['duration']
        if member_name and duration:
            members.append({
                'name': member_name,
                'duration': MEMBERSHIP_DURATIONS[duration],
                'start_date': datetime.now().date(),
                'active': True
            })
            flash('Membership added successfully!', 'success')
            return redirect(url_for('membership'))
        else:
            flash('Please fill all required fields', 'error')
    return render_template('add_membership.html')

@app.route('/update_membership', methods=['GET', 'POST'])
def update_membership():
    if 'username' not in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        member_id = request.form['member_id']
        action = request.form['action']
        if member_id and action:
            member = members[int(member_id)]
            if action == 'extend':
                duration = request.form['duration']
                member['duration'] += MEMBERSHIP_DURATIONS[duration]
                flash('Membership extended successfully!', 'success')
            elif action == 'cancel':
                member['active'] = False
                flash('Membership cancelled successfully!', 'success')
            return redirect(url_for('membership'))
        else:
            flash('Invalid request', 'error')
    return render_template('update_membership.html')

# Book Management Routes
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Add book implementation here
        flash('Book added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_book.html')

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if 'username' not in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Issue book implementation here
        flash('Book issued successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('issue_book.html')

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if 'username' not in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Return book implementation here
        flash('Book returned successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('return_book.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':

    app.run(debug=True)
