import { Admin, Resource } from "react-admin";
import { StaffList } from "./components/StaffList";
import { dataProvider } from "./dataProvider";
import { BranchList } from "./components/BranchList";
import { ClientList } from "./components/ClientList";
import { StaffCreate, StaffEdit } from "./components/CreateStaff";

export function App() {
  return (
    <Admin dataProvider={dataProvider as any}>
      <Resource
        name="staff"
        list={StaffList}
        create={StaffCreate}
        edit={StaffEdit}
      />
      <Resource name="branches" list={BranchList} />
      <Resource name="clients" list={ClientList} />
    </Admin>
  );
}
