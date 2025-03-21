import React, { useEffect, useState } from "react";
import axios from "axios";

interface Staff {
  staff_no: string;
  first_name: string;
  last_name: string;
  position: string;
  sex: string;
  dob: string | null;
  salary: number;
  branch_no: string;
  telephone: string;
  mobile?: string;
  email?: string;
}

const StaffList: React.FC = () => {
  const [staffList, setStaffList] = useState<Staff[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get<Staff[]>("http://127.0.0.1:5000/staff/list")
      .then((res) => {
        setStaffList(res.data);
        setLoading(false);
      })
      .catch((err: unknown) => {
        console.error(err);
        setError("Failed to fetch staff data.");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Staff List</h1>
      <table>
        <thead>
          <tr>
            <th>Staff No</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Position</th>
            <th>Sex</th>
            <th>DOB</th>
            <th>Salary</th>
            <th>Branch No</th>
            <th>Telephone</th>
            <th>Mobile</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {staffList.map((staff, i) => (
            <tr key={i}>
              <td>{staff.staff_no}</td>
              <td>{staff.first_name}</td>
              <td>{staff.last_name}</td>
              <td>{staff.position}</td>
              <td>{staff.sex}</td>
              <td>{staff.dob}</td>
              <td>{staff.salary}</td>
              <td>{staff.branch_no}</td>
              <td>{staff.telephone}</td>
              <td>{staff.mobile}</td>
              <td>{staff.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StaffList;