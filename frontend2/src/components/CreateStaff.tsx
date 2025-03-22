import {
  Create,
  DateInput,
  NumberInput,
  SelectInput,
  SimpleForm,
  TextInput,
} from "react-admin";

export const StaffCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="first_name" label="First Name" />
      <TextInput source="last_name" label="Last Name" />
      <TextInput source="position" label="Position" />
      <SelectInput
        source="sex"
        label="Gender"
        choices={[
          { id: "Male", name: "Male" },
          { id: "Female", name: "Female" },
        ]}
      />
      <DateInput source="dob" label="Date of Birth" />
      <NumberInput source="salary" label="Salary" />
      <TextInput source="branch_no" label="Branch Number" />
      <TextInput source="telephone" label="Telephone" />
      <TextInput source="mobile" label="Mobile" />
      <TextInput source="email" label="Email" />
    </SimpleForm>
  </Create>
);
