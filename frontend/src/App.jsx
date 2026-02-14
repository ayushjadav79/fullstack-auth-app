import React from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import Register from './pages/Register.jsx';
import UserList from './pages/UserList.jsx';
import Login from './pages/Login.jsx';

// This is the critical line for Load Balanced authentication.
// It tells Axios to send and receive cookies/tokens for every request.
axios.defaults.withCredentials = true;

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/users" element={<UserList />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;