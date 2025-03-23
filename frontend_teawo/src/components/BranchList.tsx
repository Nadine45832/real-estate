import { List, Datagrid, TextField } from "react-admin";

export const BranchList = () => (
  <List>
    <Datagrid>
      <TextField source="branch_no" />
      <TextField source="street" />
      <TextField source="city" />
      <TextField source="postcode" />
    </Datagrid>
  </List>
);
