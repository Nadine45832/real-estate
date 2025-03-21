import { List, Datagrid, TextField } from "react-admin";

export const BranchList = () => (
  <List>
    <Datagrid>
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="location" />
    </Datagrid>
  </List>
);
