import {
  List,
  Datagrid,
  TextField,
  DateField,
  NumberField,
  EmailField,
} from "react-admin";

export const StaffList = () => (
  <List>
    <Datagrid>
      <TextField source="staff_no" />
      <TextField source="first_name" />
      <TextField source="last_name" />
      <TextField source="position" />
      <TextField source="sex" />
      <DateField source="dob" label="Date of Birth" />
      <NumberField source="salary" label="Salary" />
      <TextField source="branch_no" label="Branch Number" />
      <TextField source="telephone" label="Telephone" />
      <TextField source="mobile" label="Mobile" />
      <EmailField source="email" label="Email" />
    </Datagrid>
  </List>
);
