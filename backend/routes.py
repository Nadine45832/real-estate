# routes.py
from flask import Blueprint, json, request, jsonify
from datetime import datetime
from config import get_db_connection
from flask import abort

dh_routes = Blueprint("dh_routes", __name__)

SORT_STAFF_MAP = {
    "staff_no": "STAFFNO",
    "first_name": "FNAME",
    "last_name": "LNAME",
    "position": "POSITION",
    "sex": "SEX",
    "dob": "DOB",
    "salary": "SALARY",
    "branch_no": "BRANCHNO",
    "telephone": "TELEPHONE",
    "mobile": "MOBILE",
    "email": "EMAIL",
}


SORT_BRANCH_MAP = {
    "branch_no": "BRANCHNO",
    "street": "STREET",
    "city": "CITY",
    "postcode": "POSTCODE",
}


SORT_MAP_CLIENT = {
    "client_no": "CLIENTNO",
    "first_name": "FNAME",
    "last_name": "LNAME",
    "phone": "TELNO",
    "street": "STREET",
    "city": "CITY",
    "email": "EMAIL",
    "pref_type": "PREFTYPE",
    "max_rent": "MAXRENT",
}


def get_params(map_sort: dict, default_sort: str):
    params = request.args
    sort = params.get("_sort", "").strip()
    order = params.get("_order", "").strip()

    sort_field = map_sort.get(sort, default_sort)
    sorting_by = (
        f"{sort_field} {order}" if order in ["ASC", "DESC"] else f"{sort_field} ASC"
    )

    filter_param = params.get("filter")
    if filter_param and filter_param != "undefined":
        filters = json.loads(filter_param)
    else:
        filters = {}

    mapped_filters = {
        map_sort.get(k, k): f"%{str(v).strip()}%" for k, v in filters.items() if v
    }
    try:
        limit = int(params.get("_limit", "").strip() or "10")
    except ValueError:
        limit = 10

    try:
        page = int(params.get("_page", "").strip())
    except ValueError:
        page = 1

    offset = (page - 1) * limit

    return sorting_by, limit, offset, mapped_filters


@dh_routes.route("/staff", methods=["GET"])
def list_staff():

    sorting_by, limit, offset, _ = get_params(SORT_STAFF_MAP, "STAFFNO")
    count = 0

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM DH_STAFF")
        count = cursor.fetchone()[0]

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
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
            ORDER BY {sorting_by}
            OFFSET :offset ROWS
            FETCH NEXT :limit ROWS ONLY
            """,
            {"offset": offset, "limit": limit},
        )
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

        response = jsonify(staff_list)
        response.headers.add("x-total-count", str(count))
        return response, 200


@dh_routes.route("/staff/<staff_no>", methods=["GET"])
def one_staff(staff_no):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """
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
        """,
            [staff_no],
        )

        row = cursor.fetchone()
        if not row:
            abort(404)

        return (
            jsonify(
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
            ),
            200,
        )


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
                mobile,
                email,
            ],
        )
        connection.commit()

    return jsonify({"message": "New staff successfully added."}), 201


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

    return jsonify({"message": "update staff successfully."}), 200


@dh_routes.route("/staff/<staff_no>", methods=["DELETE"])
def delete_staff(staff_no):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM DH_STAFF
            WHERE STAFFNO = :staff_no
        """,
            [staff_no],
        )
        connection.commit()

        return jsonify({"message": "staff successfully deleted"}), 200


@dh_routes.route("/branch", methods=["GET"])
def list_branches():

    sorting_by, limit, offset, _ = get_params(SORT_BRANCH_MAP, "BRANCHNO")
    count = 0

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM DH_BRANCH")
        count = cursor.fetchone()[0]

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
                SELECT 
                    BRANCHNO, 
                    STREET, 
                    CITY, 
                    POSTCODE
                FROM DH_BRANCH
                ORDER BY {sorting_by}
                OFFSET :offset ROWS
                FETCH NEXT :limit ROWS ONLY
            """,
            {"offset": offset, "limit": limit},
        )
        rows = cursor.fetchall()
        result = []
        for r in rows:
            result.append(
                {
                    "branch_no": r[0],
                    "street": r[1],
                    "city": r[2],
                    "postcode": r[3],
                }
            )
        response = jsonify(result)
        response.headers.add("x-total-count", str(count))
        return response, 200


@dh_routes.route("/branch/<branch_no>", methods=["GET"])
def get_one_branch(branch_no):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """
                    SELECT 
                    BRANCHNO, 
                    STREET, 
                    CITY, 
                    POSTCODE
                    FROM DH_BRANCH
                    WHERE BRANCHNO = :branch_no
                """,
            [branch_no],
        )
        row = cursor.fetchone()
        if not row:
            abort(404)

        return (
            jsonify(
                {
                    "branch_no": row[0],
                    "street": row[1],
                    "city": row[2],
                    "postcode": row[3],
                }
            ),
            200,
        )


@dh_routes.route("/branch/<branch_no>/address", methods=["GET"])
def get_branch_address(branch_no):
    connection = get_db_connection()

    with connection.cursor() as cursor:
        out_address = cursor.var(str)
        cursor.callproc("get_branch_address_sp", [branch_no, out_address])
    address = out_address.getvalue()
    if not address:
        return jsonify({"error": "No address found"}), 404

    return jsonify({"branch_no": branch_no, "address": address}), 200


@dh_routes.route("/branch/<branch_no>", methods=["PUT"])
def update_branch(branch_no):
    data = request.get_json() or {}

    new_street = data.get("street", "")
    new_city = data.get("city", "")
    new_postcode = data.get("postcode", "")

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.callproc(
            "update_branch_sp", [branch_no, new_street, new_city, new_postcode]
        )
        connection.commit()

    return jsonify({"message": "Branch updated successfully"}), 200


@dh_routes.route("/branch/<branch_no>", methods=["DELETE"])
def delete_branch(branch_no):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM DH_BRANCH
            WHERE BRANCHNO = :branch_no
        """,
            [branch_no],
        )
        connection.commit()

        return jsonify({"message": "Branch successfully deleted"}), 200


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


@dh_routes.route("/client", methods=["GET"])
def list_clients():

    sorting_by, limit, offset, filters = get_params(SORT_MAP_CLIENT, "CLIENTNO")
    count = 0

    if filters:
        where_clause = " AND ".join([f"{key} LIKE :{key}" for key in filters.keys()])
    else:
        where_clause = "1=1"
    where_clause = f"WHERE {where_clause}"

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM DH_CLIENT")
        count = cursor.fetchone()[0]

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
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
            {where_clause}
            ORDER BY {sorting_by}
            OFFSET :offset ROWS
            FETCH NEXT :limit ROWS ONLY
        """,
            {"offset": offset, "limit": limit, **filters},
        )
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
                "max_rent": row[8],
            }
            for row in rows
        ]

    response = jsonify(clients)
    response.headers.add("x-total-count", str(count))
    return response, 200


@dh_routes.route("/client/<client_no>", methods=["GET"])
def get_one_client(client_no):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """
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
        """,
            [client_no],
        )

        row = cursor.fetchone()
        if not row:
            abort(404)

        return (
            jsonify(
                {
                    "id": row[0],
                    "client_no": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "phone": row[3],
                    "street": row[4],
                    "city": row[5],
                    "email": row[6],
                    "pref_type": row[7],
                    "max_rent": row[8],
                }
            ),
            200,
        )


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

    return jsonify({"message": "New client created"}), 201


@dh_routes.route("/client/<client_no>", methods=["PUT"])
def update_client(client_no):
    data = request.get_json() or {}

    new_phone = data.get("phone", "").strip()
    new_email = data.get("email", "").strip()
    new_street = data.get("street", "").strip()
    new_city = data.get("city", "").strip()
    new_pref_type = data.get("pref_type", "").strip()
    new_max_rent = data.get("max_rent", 0)

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.callproc(
            "update_client_sp",
            [
                client_no,
                new_phone,
                new_email,
                new_street,
                new_city,
                new_pref_type,
                new_max_rent,
            ],
        )
        connection.commit()

    return jsonify({"message": "Client successfully updated."}), 200


@dh_routes.route("/client/<client_no>", methods=["DELETE"])
def delete_client(client_no):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM DH_CLIENT
            WHERE CLIENTNO = :client_no
        """,
            [client_no],
        )
        connection.commit()

        return jsonify({"message": "Client successfully deleted"}), 200
