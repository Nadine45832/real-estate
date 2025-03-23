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
     <TextInput source="branch_no" label="branch Number" />
     <TextInput source="street" label="street" />
     <TextInput source="city" label="city" />
     <TextInput source="postcode" label="postcode" />
    </SimpleForm>
);
export const BranchCreate = () => (
  <Create>
    <Form />
  </Create>
);
export const BranchEdit = () => (
  <Edit>
    <Form />
  </Edit>
);