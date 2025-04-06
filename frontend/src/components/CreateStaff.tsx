import { Typography } from "@mui/material";
import {
  Create,
  DateInput,
  Edit,
  NumberInput,
  ReferenceInput,
  SelectInput,
  SimpleForm,
  TextInput,
  useRecordContext,
} from "react-admin";
import { MyToolbar } from "./CustomToolbar";

const Form = () => (
  <SimpleForm>
    <TextInput source="staff_no" label="Staff #" />
    <TextInput source="first_name" label="First Name" />
    <TextInput source="last_name" label="Last Name" />
    <TextInput source="position" label="Position" />
    <SelectInput
      source="sex"
      label="Gender"
      choices={[
        { id: "M", name: "Male" },
        { id: "F", name: "Female" },
      ]}
    />
    <DateInput source="dob" label="Date of Birth" />
    <NumberInput source="salary" label="Salary" />
    <ReferenceInput
      source="branch_no"
      reference="branch"
      label="Branch Number"
    />
    <TextInput source="telephone" label="Telephone" />
    <TextInput source="mobile" label="Mobile" />
    <TextInput source="email" label="Email" />
  </SimpleForm>
);

export const StaffCreate = () => (
  <Create>
    <Form />
  </Create>
);

export const StaffEdit = () => (
  <Edit>
    <EditStaffForm />
  </Edit>
);

const EditStaffForm = () => {
  const record = useRecordContext();

  return (
    <div>
      <div style={{ margin: "1em" }}>
        <Typography variant="h3">{`${record.first_name} ${record.last_name}`}</Typography>
        <Typography variant="body2">Position: {record.position}</Typography>
        <Typography variant="body2">Branch: {record.branch_no}</Typography>
      </div>
      <SimpleForm toolbar={<MyToolbar />}>
        <NumberInput source="salary" label="Salary" />
        <TextInput source="telephone" label="Telephone" />
        <TextInput source="email" label="Email" />
      </SimpleForm>
    </div>
  );
};
