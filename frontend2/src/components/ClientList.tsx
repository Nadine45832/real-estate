import { List, Datagrid, TextField } from "react-admin";

export const ClientList = () => (
  <List>
    <Datagrid>
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="email" />
    </Datagrid>
  </List>
);
