import { Admin, Resource } from "react-admin";
import jsonServerProvider from "ra-data-json-server";
import { StaffList } from "./components/StaffList";
import { BranchList } from "./components/BranchList";
import { ClientList } from "./components/ClientList";

const dataProvider = jsonServerProvider("http://localhost:8000"); // Flask API endpoint

export function App() {
  return (
    <Admin dataProvider={dataProvider}>
      <Resource name="staff" list={StaffList} />
      <Resource name="branches" list={BranchList} />
      <Resource name="clients" list={ClientList} />
    </Admin>
  );
}
