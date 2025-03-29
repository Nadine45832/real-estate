import { Create, Edit, NumberInput, SimpleForm, TextInput } from "react-admin";

const Form = () => (
  <SimpleForm>
    <TextInput source="first_name" label="First Name" />
    <TextInput source="last_name" label="Last Name" />
    <TextInput source="phone" label="Phone number" />
    <TextInput source="street" label="Street" />
    <TextInput source="city" label="City" />
    <TextInput source="email" label="Email" />
    <TextInput source="pref_type" label="Pref Type" />
    <NumberInput source="max_rent" label="Max Rent" />
  </SimpleForm>
);

export const ClientCreate = () => (
  <Create>
    <Form />
  </Create>
);

export const ClientEdit = () => (
  <Edit>
    <Form />
  </Edit>
);
