from flask import Blueprint, request, jsonify
from backend.models import Branch, Staff, Client

routes_dh = Blueprint("routes", __name__)


@routes_dh.route("/branches", methods=["GET", "POST"])
def get_branches():
    if request.method == "POST":
        data = request.json
        new_branch = Branch(name=data["name"], location=data["location"])
        db.session.add(new_branch)
        db.session.commit()
        return jsonify({"message": "Branch created"}), 201
    branches = Branch.query.all()
    return jsonify(
        [{"id": b.id, "name": b.name, "location": b.location} for b in branches]
    )


@routes_dh.route("/branches", methods=["PUT"])
def add_branches():
    data = request.json
    new_branch = Branch(name=data["name"], location=data["location"])
    db.session.add(new_branch)
    db.session.commit()
    return jsonify({"message": "Branch created"}), 201


@routes_dh.route("/staff", methods=["GET"])
def get_staff():
    staff = Staff.query.all()
    return jsonify(
        [
            {"id": s.id, "name": s.name, "role": s.role, "branch_id": s.branch_id}
            for s in staff
        ]
    )


@routes_dh.route("/staff", methods=["PUT"])
def add_staff():
    data = request.json
    new_staff = Staff(name=data["name"], role=data["role"], branch_id=data["branch_id"])
    db.session.add(new_staff)
    db.session.commit()
    return jsonify({"message": "Staff member added"}), 201


@routes_dh.route("/client", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    return jsonify([{"id": c.id, "name": c.name, "email": c.email} for c in clients])


@routes_dh.route("/client", methods=["PUT"])
def add_clients():
    data = request.json
    new_client = Client(name=data["name"], email=data["email"])
    db.session.add(new_client)
    db.session.commit()
    return jsonify({"message": "Client added"}), 201
