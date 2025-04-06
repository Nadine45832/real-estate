import { Typography } from "@mui/material";
import {
  Create,
  Edit,
  NumberInput,
  SimpleForm,
  TextInput,
  useRecordContext,
} from "react-admin";
import { MyToolbar } from "./CustomToolbar";

const Form = () => (
  <SimpleForm>
    <TextInput source="client_no" label="Client #" />
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
    <EditClientForm />
  </Edit>
);

const EditClientForm = () => {
  const record = useRecordContext();

  return (
    <div>
      <div style={{ margin: "1em" }}>
        <Typography variant="h3">{`Client ${record.first_name} ${record.last_name}`}</Typography>
      </div>
      <SimpleForm toolbar={<MyToolbar />}>
        <TextInput source="phone" label="Phone number" />
        <TextInput source="street" label="Street" />
        <TextInput source="city" label="City" />
        <TextInput source="email" label="Email" />
        <TextInput source="pref_type" label="Pref Type" />
        <NumberInput source="max_rent" label="Max Rent" />
      </SimpleForm>
    </div>
  );
};
