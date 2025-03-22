# routes.py
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
import oracledb
from datetime import datetime
from config import get_db_connection

dh_routes = Blueprint("dh_routes", __name__)


@dh_routes.route("/staff", methods=["GET"])
def list_staff():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "DB connection failed"}), 500
        cursor = connection.cursor()
        query = """
            SELECT 
                STAFFNO, 
                FNAME, 
                LNAME, 
                POSITION, 
                SEX, 
                TO_CHAR(DOB, 'YYYY-MM-DD') AS DOB, 
                SALARY, 
                BRANCHNO, 
                TELEPHONE,
                NVL(MOBILE, '') AS MOBILE,
                NVL(EMAIL, '') AS EMAIL
            FROM DH_STAFF
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        staff_list = []
        for row in rows:
            staff_list.append(
                {
                    "staff_no": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "position": row[3],
                    "sex": row[4],
                    "dob": row[5],
                    "salary": row[6],
                    "branch_no": row[7],
                    "telephone": row[8],
                    "mobile": row[9],
                    "email": row[10],
                }
            )
        return jsonify(staff_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@dh_routes.route("/staff/<staff_no>", methods=["GET"])
def one_staff(staff_no):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "DB connection failed"}), 500
        cursor = connection.cursor()
        query = """
            SELECT 
                STAFFNO, 
                FNAME, 
                LNAME, 
                POSITION, 
                SEX, 
                TO_CHAR(DOB, 'YYYY-MM-DD') AS DOB, 
                SALARY, 
                BRANCHNO, 
                TELEPHONE,
                NVL(MOBILE, '') AS MOBILE,
                NVL(EMAIL, '') AS EMAIL
            FROM DH_STAFF
            WHERE STAFFNO = :staff_no
        """
        cursor.execute(query, [staff_no])
        row = cursor.fetchone()
        val = {
            "staff_no": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "position": row[3],
            "sex": row[4],
            "dob": row[5],
            "salary": row[6],
            "branch_no": row[7],
            "telephone": row[8],
            "mobile": row[9],
            "email": row[10],
        }
        return jsonify(val), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@dh_routes.route("/staff", methods=["PUT"])
def hire_staff():
    data = request.form if request.form else request.json

    staff_no = data.get("staff_no", "").strip()
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    position = data.get("position", "").strip()
    sex = data.get("sex", "").strip()
    dob_str = data.get("dob", "").strip()
    salary_str = data.get("salary", "0").strip()
    branch_no = data.get("branch_no", "").strip()
    telephone = data.get("telephone", "").strip()

    # Convert date
    dob = None
    if dob_str:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")

    # Convert salary
    salary = int(salary_str) if salary_str.isdigit() else 0

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "DB connection failed"}), 500
        cursor = connection.cursor()

        # Call staff_hire_sp
        cursor.callproc(
            "staff_hire_sp",
            [
                staff_no,
                first_name,
                last_name,
                position,
                sex,
                dob,
                salary,
                branch_no,
                telephone,
            ],
        )

        connection.commit()
        return jsonify({"message": "Staff hired successfully"}), 201

    except oracledb.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@dh_routes.route("/staff/update", methods=["POST"])
def update_staff():
    data = request.form if request.form else request.json

    staff_no = data.get("staff_no", "").strip()
    new_salary_str = data.get("new_salary", "0").strip()
    new_telephone = data.get("new_telephone", "").strip()
    new_email = data.get("new_email", "").strip()

    new_salary = int(new_salary_str) if new_salary_str.isdigit() else 0

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "DB connection failed"}), 500
        cursor = connection.cursor()

        # Call update_staff_sp
        cursor.callproc(
            "update_staff_sp", [staff_no, new_salary, new_telephone, new_email]
        )

        connection.commit()
        return jsonify({"message": "Staff updated successfully"}), 200

    except oracledb.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@dh_routes.route("/branch/get_address", methods=["GET"])
def get_branch_address():
    branch_no = request.args.get("branch_no", "").strip()
    if not branch_no:
        return jsonify({"error": "branch_no is required"}), 400

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "DB connection failed"}), 500
        cursor = connection.cursor()

        # Use SELECT get_branch_address_fn(...) FROM DUAL
        cursor.execute("SELECT get_branch_address_fn(:bno) FROM DUAL", bno=branch_no)
        row = cursor.fetchone()
        if row:
            address = row[0]
            return jsonify({"branch_no": branch_no, "address": address}), 200
        else:
            return jsonify({"message": "No address found"}), 404

    except oracledb.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@dh_routes.route("/branch/update", methods=["POST"])
def update_branch():
    data = request.form if request.form else request.json

    branch_no = data.get("branch_no", "").strip()
    new_street = data.get("new_street", "").strip()
    new_city = data.get("new_city", "").strip()
    new_postcode = data.get("new_postcode", "").strip()

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "DB connection failed"}), 500
        cursor = connection.cursor()

        # Call update_branch_sp
        cursor.callproc(
            "update_branch_sp", [branch_no, new_street, new_city, new_postcode]
        )

        connection.commit()
        return jsonify({"message": "Branch updated successfully"}), 200

    except oracledb.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@dh_routes.route("/branch/new", methods=["POST"])
def new_branch():
    data = request.form if request.form else request.json

    branch_no = data.get("branch_no", "").strip()
    street = data.get("street", "").strip()
    city = data.get("city", "").strip()
    postcode = data.get("postcode", "").strip()

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "DB connection failed"}), 500
        cursor = connection.cursor()

        # Call new_branch_sp
        cursor.callproc("new_branch_sp", [branch_no, street, city, postcode])

        connection.commit()
        return jsonify({"message": "New branch created"}), 201

    except oracledb.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@dh_routes.route("/client/new", methods=["POST"])
def new_client():
    data = request.form if request.form else request.json

    client_no = data.get("client_no", "").strip()
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    phone = data.get("phone", "").strip()
    street = data.get("street", "").strip()
    city = data.get("city", "").strip()
    email = data.get("email", "").strip()
    pref_type = data.get("pref_type", "").strip()
    max_rent_str = data.get("max_rent", "0").strip()
    max_rent = int(max_rent_str) if max_rent_str.isdigit() else 0

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "DB connection failed"}), 500
        cursor = connection.cursor()

        cursor.callproc(
            "new_client_sp",
            [
                client_no,
                first_name,
                last_name,
                phone,
                street,
                city,
                email,
                pref_type,
                max_rent,
            ],
        )

        connection.commit()
        return jsonify({"message": "New client registered"}), 201

    except oracledb.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@dh_routes.route("/client/update", methods=["POST"])
def update_client():
    data = request.form if request.form else request.json

    client_no = data.get("client_no", "").strip()
    new_phone = data.get("new_phone", "").strip()
    new_email = data.get("new_email", "").strip()
    new_city = data.get("new_city", "").strip()

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "DB connection failed"}), 500
        cursor = connection.cursor()

        cursor.callproc("update_client_sp", [client_no, new_phone, new_email, new_city])

        connection.commit()
        return jsonify({"message": "Client updated"}), 200

    except oracledb.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
