# routes.py
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
import oracledb
from datetime import datetime
from config import get_db_connection

dh_routes = Blueprint("dh_routes", __name__)


@dh_routes.route("/staff", methods=["GET"])
def list_staff():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
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
        """)
        rows = cursor.fetchall()

        staff_list = [
            {
                "id": row[0],
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
            for row in rows
        ]

        return jsonify(staff_list), 200



from flask import abort

@dh_routes.route("/staff/<staff_no>", methods=["GET"])
def one_staff(staff_no):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
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
                NVL(MOBILE, ''), 
                NVL(EMAIL, '')
            FROM DH_STAFF
            WHERE STAFFNO = :staff_no
        """, [staff_no])

        row = cursor.fetchone()
        if not row:
            abort(404)

        return jsonify({
            "id": row[0],
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
        }), 200



@dh_routes.route("/staff", methods=["POST"])
def hire_staff():
    data = request.get_json() or {}

    # dob and salary convert
    dob = datetime.fromisoformat(data["dob"][:10]) if "dob" in data else None
    salary = int(data.get("salary", 0))
    connection = get_db_connection()

    with connection.cursor() as cursor:
        # Create staff number
        cursor.execute("""
            SELECT MAX(TO_NUMBER(STAFFNO)) FROM DH_STAFF
            WHERE REGEXP_LIKE(STAFFNO, '^[0-9]+$')
        """)
        max_id = cursor.fetchone()[0]
        new_id = int(max_id) + 1 if max_id else 1
        staff_no = str(new_id)

        # Call procedure
        cursor.callproc("staff_hire_sp", [
            staff_no,
            data["first_name"],
            data["last_name"],
            data["position"],
            data["sex"],
            dob,
            salary,
            data["branch_no"],
            data["telephone"],
            data.get("mobile", ""),
            data.get("email", "")
        ])
        connection.commit()

    return jsonify({ "New staff successfully added." }), 201




@dh_routes.route("/staff/<staff_no>", methods=["PUT"])
def update_staff(staff_no):
    data = request.get_json() or {}

    # only these fields are required according to the instruction
    salary = int(data.get("salary", 0))
    telephone = data.get("telephone", "")
    email = data.get("email", "")

    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Call precedure
        cursor.callproc("update_staff_sp", [staff_no, salary, telephone, email])
        connection.commit()

    return jsonify({
        "id": staff_no,
        "staff_no": staff_no,
        "salary": salary,
        "telephone": telephone,
        "email": email
    }), 200


@dh_routes.route("/branches", methods=["GET"])
def list_branches():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT 
                    BRANCHNO, 
                    STREET, 
                    CITY, 
                    POSTCODE
                    FROM DH_BRANCH
                """)
        rows = cursor.fetchall()
        result=[]
        for r in rows:
            result.append({
                "branch_no": r[0],
                "street": r[1],
                "city": r[2],
                "postcode": r[3],
            })
        return jsonify(result), 200

@dh_routes.route("/branch/<branch_no>", methods=["GET"])
def get_one_branch(branch_no):
    connection = get_db_connection()

    with connection.cursor() as cursor:
        out_address = cursor.var(str)
    cursor.callproc("get_branch_address_sp", [branch_no, out_address])
    address = out_address.getvalue()
    if not address:
        return jsonify({"error": "No address found"}), 404

    return jsonify({
        "branch_no": branch_no,
        "address": address
    }), 200

@dh_routes.route("/branch/<branch_no>", methods=[""])
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
