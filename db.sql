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