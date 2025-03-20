from flask import Flask, render_template, request, redirect, url_for, flash
import cx_Oracle
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
from config import get_db_connection
app = Flask(__name__)

# Staff Register API
@app.route('/hire_staff', methods=['POST'])
def hire_staff():
    if request.method == 'POST':
        staff_no = request.form['staff_no']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position = request.form['position']
        sex = request.form['sex']
        dob = request.form['dob']
        salary = request.form['salary']
        branch_no = request.form['branch_no']
        telephone = request.form['telephone']

        try:
            connection = get_db_connection()    # Connection Oracle DB
            cursor = connection.cursor()

            cursor.callproc("staff_hire_sp", [
                staff_no, first_name, last_name, position, sex, dob, salary, branch_no, telephone
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
    app.secret_key = 'your_secret_key'  # Flash 메시지를 사용하기 위한 Secret Key
    app.run(debug=True)