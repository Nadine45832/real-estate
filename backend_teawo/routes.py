# routes.py
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
import oracledb
from datetime import datetime
from config import get_db_connection
from flask import abort

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

    staff_no = data.get("staff_no", "").strip()
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    position = data.get("position", "").strip()
    sex = data.get("sex", "").strip()
    dob_str = data.get("dob", "").strip()
    dob = datetime.fromisoformat(dob_str) if dob_str else None
    salary = int(data.get("salary", 0))
    branch_no = data.get("branch_no", "").strip()
    telephone = data.get("telephone", "").strip()
    mobile = data.get("mobile", "").strip()
    email = data.get("email", "").strip()

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.callproc("staff_hire_sp", [
            staff_no,
            first_name,
            last_name,
            position,
            sex,
            dob,
            salary,
            branch_no,
            telephone,
            mobile,
            email
        ])
        connection.commit()

    return jsonify({ "message": "New staff successfully added." }), 201





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

    return jsonify({ 'message': 'update staff successfully.' }), 200


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

@dh_routes.route("/branch/<branch_no>", methods=["PUT"])
def update_branch(branch_no):
    data = request.get_json() or {}

    new_street = data.get("street", "")
    new_city = data.get("city", "")
    new_postcode = data.get("postcode", "")

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.callproc("update_branch_sp", [branch_no, new_street, new_city, new_postcode])
        connection.commit()

    return jsonify({"message": "Branch updated successfully"}), 200



@dh_routes.route("/branch", methods=["POST"])
def new_branch():
    data = request.get_json() or {}

    branch_no = data.get("branch_no", "").strip()
    street = data.get("street", "").strip()
    city = data.get("city", "").strip()
    postcode = data.get("postcode", "").strip()

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.callproc("new_branch", [branch_no, street, city, postcode])
        connection.commit()

    return jsonify({"message": "New branch created"}), 201



@dh_routes.route("/clients", methods=["GET"])
def list_clients():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                CLIENTNO, 
                FNAME, 
                LNAME, 
                TELNO, 
                STREET, 
                CITY, 
                EMAIL, 
                PREFTYPE, 
                MAXRENT
            FROM DH_CLIENT
        """)
        rows = cursor.fetchall()

        clients = [
            {
                "id": row[0],  # for React Admin
                "client_no": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "phone": row[3],
                "street": row[4],
                "city": row[5],
                "email": row[6],
                "pref_type": row[7],
                "max_rent": row[8]
            }
            for row in rows
        ]

    return jsonify(clients), 200


@dh_routes.route("/client/<client_no>", methods=["GET"])
def get_one_client(client_no):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                CLIENTNO, 
                FNAME, 
                LNAME, 
                TELNO, 
                STREET, 
                CITY, 
                EMAIL, 
                PREFTYPE, 
                MAXRENT
            FROM DH_CLIENT
            WHERE CLIENTNO = :client_no
        """, [client_no])

        row = cursor.fetchone()
        if not row:
            abort(404)

        return jsonify({
            "id": row[0],
            "client_no": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "phone": row[3],
            "street": row[4],
            "city": row[5],
            "email": row[6],
            "pref_type": row[7],
            "max_rent": row[8]
        }), 200

@dh_routes.route("/client", methods=["POST"])
def new_client():
    data = request.get_json() or {}

    client_no = data.get("client_no", "").strip()
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    phone = data.get("phone", "").strip()
    street = data.get("street", "").strip()
    city = data.get("city", "").strip()
    email = data.get("email", "").strip()
    pref_type = data.get("pref_type", "").strip()
    max_rent = int(data.get("max_rent", 0))

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.callproc("new_client_sp", [
            client_no,
            first_name,
            last_name,
            phone,
            street,
            city,
            email,
            pref_type,
            max_rent
        ])
        connection.commit()

    return jsonify({ "message": "New client created" }), 201



@dh_routes.route("/client/<client_no>", methods=["PUT"])
def update_client(client_no):
    data = request.get_json() or {}

    new_phone = data.get("phone", "").strip()
    new_email = data.get("email", "").strip()
    new_city = data.get("city", "").strip()

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.callproc("update_client_sp", [
            client_no,
            new_phone,
            new_email,
            new_city
        ])
        connection.commit()

    return jsonify({ "message": "Client successfully updated." }), 200
