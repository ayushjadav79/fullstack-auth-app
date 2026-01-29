import React, { useEffect, useState } from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Register from './pages/Register.jsx';
import UserList from './pages/UserList.jsx';
import Login from './pages/Login.jsx';

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