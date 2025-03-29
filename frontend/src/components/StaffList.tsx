import {
  List,
  Datagrid,
  TextField,
  DateField,
  NumberField,
  EmailField,
  ReferenceField,
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
      <ReferenceField source="branch_no" reference="branch" label="Branch" />
      <TextField source="telephone" label="Telephone" />
      <TextField source="mobile" label="Mobile" />
      <EmailField source="email" label="Email" />
    </Datagrid>
  </List>
);
