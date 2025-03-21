from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Staff(db.Model):
    __tablename__ = "DH_STAFF"

    staff_no = db.Column(db.String(50), primary_key=True, name="STAFFNO")
    first_name = db.Column(db.String(50), nullable=False, name="FNAME")
    last_name = db.Column(db.String(50), nullable=False, name="LNAME")
    position = db.Column(db.String(50), nullable=False, name="POSITION")
    sex = db.Column(db.String(50), name="SEX")
    dob = db.Column(db.Date, nullable=False, name="DOB")
    salary = db.Column(db.Float, nullable=False, name="SALARY")
    branch_no = db.Column(db.String(50), nullable=False, name="BRANCHNO")
    telephone = db.Column(db.String(16), name="TELEPHONE")
    mobile = db.Column(db.String(16), name="MOBILE")
    email = db.Column(db.String(50), name="EMAIL")


class Branch(db.Model):
    __tablename__ = "DH_BRANCH"

    branch_no = db.Column(db.String(50), primary_key=True, name="BRANCHNO")
    street = db.Column(db.String(50), name="STREET")
    city = db.Column(db.String(50), name="CITY")
    postcode = db.Column(db.String(20), name="POSTCODE")


class Client(db.Model):
    __tablename__ = "DH_CLIENT"

    client_no = db.Column(db.String(50), primary_key=True, name="CLIENTNO")
    first_name = db.Column(db.String(30), nullable=False, name="FNAME")
    last_name = db.Column(db.String(30), nullable=False, name="LNAME")
    phone = db.Column(db.String(20), name="TELNO")
    street = db.Column(db.String(30), name="STREET")
    city = db.Column(db.String(30), name="CITY")
    email = db.Column(db.String(40), name="EMAIL")
    pref_type = db.Column(db.String(5), name="PREFTYPE")
    max_rent = db.Column(db.Numeric(38, 0), name="MAXRENT")


class Lease(db.Model):
    __tablename__ = "DH_LEASE"

    lease_no = db.Column(db.Integer, primary_key=True, name="LEASENO")
    client_no = db.Column(
        db.String(50), db.ForeignKey("DH_CLIENT.CLIENTNO"), name="CLIENTNO"
    )
    property_no = db.Column(db.String(10), name="PROPERTYNO")
    lease_amount = db.Column(db.Numeric(9, 2), name="LEASEAMOUNT")
    lease_start = db.Column(db.Date, name="LEASE_START")
    lease_end = db.Column(db.Date, name="LEASE_END")


class PropertyForRent(db.Model):
    __tablename__ = "DH_PROPERTYFORRENT"

    property_no = db.Column(db.String(10), primary_key=True, name="PROPERTYNO")
    street = db.Column(db.String(50), name="STREET")
    city = db.Column(db.String(50), name="CITY")
    postcode = db.Column(db.String(50), name="POSTCODE")
    type = db.Column(db.String(50), name="TYPE")
    rooms = db.Column(db.Integer, name="ROOMS")
    rent = db.Column(db.Numeric(7, 0), name="RENT")
    owner_no = db.Column(db.String(5), name="OWNERNO")
    staff_no = db.Column(db.String(50), name="STAFFNO")
    branch_no = db.Column(db.String(50), name="BRANCHNO")
    picture = db.Column(db.String(50), name="PICTURE")
    floorplan = db.Column(db.String(100), name="FLOORPLAN")


class Registration(db.Model):
    __tablename__ = "DH_REGISTRATION"

    client_no = db.Column(
        db.String(50),
        db.ForeignKey("DH_CLIENT.CLIENTNO"),
        primary_key=True,
        name="CLIENTNO",
    )
    branch_no = db.Column(
        db.String(50),
        db.ForeignKey("DH_BRANCH.BRANCHNO"),
        primary_key=True,
        name="BRANCHNO",
    )
    staff_no = db.Column(
        db.String(50), db.ForeignKey("DH_STAFF.STAFFNO"), name="STAFFNO"
    )
    date_register = db.Column(db.Date, name="DATEREGISTER")


class PrivateOwner(db.Model):
    __tablename__ = "DH_PRIVATEOWNER"

    owner_no = db.Column(db.String(5), primary_key=True, name="OWNERNO")
    first_name = db.Column(db.String(10), name="FNAME")
    last_name = db.Column(db.String(10), name="LNAME")
    address = db.Column(db.String(50), name="ADDRESS")
    tel_no = db.Column(db.String(15), name="TELNO")
    email = db.Column(db.String(50), name="EMAIL")
    password = db.Column(db.String(40), name="PASSWORD")


class Viewing(db.Model):
    __tablename__ = "DH_VIEWING"

    client_no = db.Column(
        db.String(50),
        db.ForeignKey("DH_CLIENT.CLIENTNO"),
        primary_key=True,
        name="CLIENTNO",
    )
    property_no = db.Column(
        db.String(10),
        db.ForeignKey("DH_PROPERTYFORRENT.PROPERTYNO"),
        primary_key=True,
        name="PROPERTYNO",
    )
    view_date = db.Column(db.Date, name="VIEWDATE")
    comments = db.Column(db.String(200), name="COMMENTS")
