import {
  List,
  Datagrid,
  TextField,
  NumberField,
  EmailField,
  SelectInput,
  TextInput,
} from "react-admin";

const getClientFilter = () => [
  <TextInput key="city" label="City" source="filters.city" alwaysOn />,
  <TextInput label="Street" source="filters.street" key="street" />,
  <TextInput label="First Name" source="filters.first_name" key="first_name" />,
];

export const ClientList = () => (
  <List filters={getClientFilter()}>
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
