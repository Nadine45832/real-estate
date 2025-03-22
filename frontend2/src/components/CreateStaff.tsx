import {
  Create,
  DateInput,
  Edit,
  NumberInput,
  SelectInput,
  SimpleForm,
  TextInput,
} from "react-admin";

const Form = () => (
  <SimpleForm>
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
    <TextInput source="branch_no" label="Branch Number" />
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
    <Form />
  </Edit>
);
