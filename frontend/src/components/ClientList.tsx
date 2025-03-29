import {
  List,
  Datagrid,
  TextField,
  NumberField,
  EmailField,
} from "react-admin";

export const ClientList = () => (
  <List>
    <Datagrid>
      <TextField source="client_no" />
      <TextField source="first_name" />
      <TextField source="last_name" />
      <TextField source="phone" />
      <TextField source="street" />
      <TextField source="city" />
      <EmailField source="email" />
      <TextField source="pref_type" />
      <NumberField source="max_rent" />
    </Datagrid>
  </List>
);
