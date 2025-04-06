import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Cancel from "@mui/icons-material/Cancel";

import { Toolbar, SaveButton, DeleteButton } from "react-admin";

export const MyToolbar = () => (
  <Toolbar
    style={{ display: "flex", gap: "1em", justifyContent: "space-between" }}
  >
    <SaveButton label="SAVE" />
    <div style={{ display: "flex", gap: "2em" }}>
      <BackButton />
      <DeleteButton label="DELETE" />
    </div>
  </Toolbar>
);

const BackButton = () => {
  const navigate = useNavigate();
  return (
    <Button
      variant="outlined"
      onClick={() => navigate(-1)}
      style={{
        display: "flex",
        borderRadius: "1em",
        fontWeight: "bold",
        border: "#000",
      }}
      startIcon={<Cancel />}
    >
      CANCEL
    </Button>
  );
};
