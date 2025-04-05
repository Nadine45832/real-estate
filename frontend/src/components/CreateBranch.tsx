import { Typography } from "@mui/material";
import {
  Create,
  Edit,
  SimpleForm,
  TextInput,
  useRecordContext,
} from "react-admin";

const Form = () => (
  <SimpleForm>
    <TextInput source="branch_no" label="Branch #" />
    <TextInput source="street" label="Street" />
    <TextInput source="city" label="City" />
    <TextInput source="postcode" label="Postcode" />
  </SimpleForm>
);
export const BranchCreate = () => (
  <Create>
    <Form />
  </Create>
);
export const BranchEdit = () => (
  <Edit>
    <EditBranchForm />
  </Edit>
);

const EditBranchForm = () => {
  const record = useRecordContext();

  return (
    <div>
      <div style={{ margin: "1em" }}>
        <Typography variant="h3">{`Branch #${record.branch_no}`}</Typography>
      </div>
      <SimpleForm>
        <TextInput source="street" label="Street" />
        <TextInput source="city" label="City" />
        <TextInput source="postcode" label="Postcode" />
      </SimpleForm>
    </div>
  );
};
