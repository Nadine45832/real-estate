from flask import Flask, render_template, request, redirect, url_for, flash
import cx_Oracle
import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))    # set current directory in order to import config.py
sys.path.append(os.path.dirname(current_dir))
from config import get_db_connection
app = Flask(__name__)

# Staff Register API
@app.route('/hire_staff', methods=['POST'])
def hire_staff():
    if request.method == 'POST':
        staff_no = request.form.get('staff_no', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        position = request.form.get('position', '').strip()
        sex = request.form.get('sex', '').strip()
        branch_no = request.form.get('branch_no', '').strip()
        telephone = request.form.get('telephone', '').strip()
        mobile = request.form.get('mobile', '').strip()
        email = request.form.get('email', '').strip()
        # Make sure user type staff_no
        if not staff_no:
            flash("You must type Staff Number.", "danger")
            return redirect(url_for('index'))
        # Convert dob string to datetime format
        dob_str = request.form.get('dob', '').strip()
        dob = datetime.strptime(dob_str, '%Y-%m-%d') if dob_str else None
        # Convert salary string to int format
        salary = request.form.get('salary', '').strip()
        salary = int(salary) if salary.isdigit() else 0

        connection = None
        cursor = None
        try:
            connection = get_db_connection()    # Connection Oracle DB
            cursor = connection.cursor()

            cursor.callproc("staff_hire_sp", [
                staff_no, first_name, last_name, position, sex, dob, salary, branch_no, telephone,
            ])

            connection.commit()
            cursor.close()
            connection.close()

            flash("Staff Successfully added.", "success")
            return redirect(url_for('index'))
        except cx_Oracle.DatabaseError as e:
            flash(f" failed to add staff: {e}", "danger")
            return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('hire_staff.html')

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)