import { Admin, Resource } from "react-admin";
import { StaffList } from "./components/StaffList";
import { dataProvider } from "./dataProvider";
import { BranchList } from "./components/BranchList";
import { ClientList } from "./components/ClientList";
import { StaffCreate, StaffEdit } from "./components/CreateStaff";
import { BranchCreate, BranchEdit } from "./components/CreateBranch";
import { ClientCreate, ClientEdit } from "./components/CreateClient";

export function App() {
  return (
    <Admin dataProvider={dataProvider as any}>
      <Resource
        name="staff"
        list={StaffList}
        create={StaffCreate}
        edit={StaffEdit}
      />
      <Resource
        name="branch"
        list={BranchList}
        create={BranchCreate}
        edit={BranchEdit}
      />
      <Resource
        name="client"
        list={ClientList}
        create={ClientCreate}
        edit={ClientEdit}
      />
    </Admin>
  );
}
