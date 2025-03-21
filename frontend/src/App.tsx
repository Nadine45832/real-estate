import React from 'react';
import './App.css';
import StaffList from './components/StaffList';

function App() {
  return (
    <div className="App">
      <h1>Staff Management</h1> {/* ✅ Testing Staff List */}
      <StaffList /> {/* ✅ Staff List rendering */}
    </div>
  );
}
export default App;
