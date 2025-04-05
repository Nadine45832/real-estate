CREATE OR REPLACE PROCEDURE staff_hire_sp (
    p_staff_no IN VARCHAR2,
    p_first_name IN VARCHAR2,
    p_last_name IN VARCHAR2,
    p_position IN VARCHAR2,
    p_sex IN VARCHAR2,
    p_dob IN DATE,
    p_salary IN NUMBER,
    p_branch_no IN VARCHAR2,
    p_telephone IN VARCHAR2,
    p_mobile IN VARCHAR2,
    p_email IN VARCHAR2
) AS
BEGIN
    INSERT INTO DH_STAFF (
        STAFFNO, FNAME, LNAME, POSITION, SEX, DOB, SALARY, BRANCHNO, TELEPHONE, MOBILE, EMAIL
    ) VALUES (
        p_staff_no, p_first_name, p_last_name, p_position, p_sex, p_dob, p_salary, p_branch_no, p_telephone, p_mobile, p_email
    );
COMMIT;
END;

/

CREATE OR REPLACE PROCEDURE update_staff_sp (
    p_staff_no IN VARCHAR2,
    p_new_salary IN NUMBER,
    p_new_telephone IN VARCHAR2,
    p_new_email IN VARCHAR2
) AS
BEGIN
    UPDATE DH_STAFF
    SET SALARY = p_new_salary, TELEPHONE = p_new_telephone, EMAIL = p_new_email
    WHERE STAFFNO = p_staff_no;
COMMIT;
END;

/

CREATE OR REPLACE FUNCTION get_branch_address_fn (
    p_branch_no IN VARCHAR2
) RETURN VARCHAR2
IS
    v_address VARCHAR2(200);
BEGIN
    SELECT STREET || ', ' || CITY INTO v_address
    FROM DH_BRANCH
    WHERE BRANCHNO = p_branch_no;
    RETURN v_address;
END;

/

CREATE OR REPLACE PROCEDURE new_branch (
    p_branch_no IN VARCHAR2,
    p_new_street IN VARCHAR2,
    p_new_city IN VARCHAR2,
    p_new_postcode IN VARCHAR2
) AS
BEGIN
    INSERT INTO DH_BRANCH (
        BRANCHNO, STREET, CITY, POSTCODE
    ) VALUES (
        p_branch_no, p_new_street, p_new_city, p_new_postcode
    );
COMMIT;
END;

/

CREATE OR REPLACE PROCEDURE update_branch_sp (
    p_branch_no IN VARCHAR2,
    p_new_street IN VARCHAR2,
    p_new_city IN VARCHAR2,
    p_new_postcode IN VARCHAR2
) AS
BEGIN
    UPDATE DH_BRANCH
    SET STREET = p_new_street, CITY = p_new_city, POSTCODE = p_new_postcode
    WHERE BRANCHNO = p_branch_no;
COMMIT;
END;

/

CREATE OR REPLACE PROCEDURE new_client_sp (
    p_client_no IN VARCHAR2,
    p_first_name IN VARCHAR2,
    p_last_name IN VARCHAR2,
    p_phone IN VARCHAR2,
    p_street IN VARCHAR2,
    p_city IN VARCHAR2,
    p_email IN VARCHAR2,
    p_pref_type IN VARCHAR2,
    p_max_rent IN NUMBER
) AS
BEGIN
    INSERT INTO DH_CLIENT (
        CLIENTNO, FNAME, LNAME, TELNO, STREET, CITY, EMAIL, PREFTYPE, MAXRENT
    ) VALUES (
        p_client_no, p_first_name, p_last_name, p_phone, p_street, p_city, p_email, p_pref_type, p_max_rent
    );
COMMIT;
END;

/

CREATE OR REPLACE PROCEDURE update_client_sp (
    p_client_no IN VARCHAR2,
    p_new_phone IN VARCHAR2,
    p_new_email IN VARCHAR2,
    p_new_street IN VARCHAR2,
    p_new_city IN VARCHAR2,
    p_new_perf_type IN VARCHAR2,
    p_new_max_rent IN NUMBER
) AS
BEGIN
    UPDATE DH_CLIENT
    SET TELNO = p_new_phone, STREET = p_new_street, CITY = p_new_city, EMAIL = p_new_email, PREFTYPE = p_new_perf_type, MAXRENT = p_new_max_rent
    WHERE CLIENTNO = p_client_no;
COMMIT;
END;