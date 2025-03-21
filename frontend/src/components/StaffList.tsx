import { List, Datagrid, TextField, ReferenceField } from "react-admin";

export const StaffList = () => (
  <List>
    <Datagrid>
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="role" />
      <ReferenceField label="Branch" source="branch_id" reference="branches">
        <TextField source="name" />
      </ReferenceField>
    </Datagrid>
  </List>
);
