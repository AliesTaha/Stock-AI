import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Signup from "./client-components/Signup";
import Login from "./client-components/Login";

const user = localStorage.getItem("token");
const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/home" element={<App />} />
        <Route path="/" element= {<App />} />
        <Route path="/signup" exact element={<Signup />} />
        <Route path="/login" exact element={<Login />} />

        {user && <Route path="/" exact element={<App />} />}
        {user && <Route path="/login" exact element={<App />} />}
        {user && <Route path="/signup" exact element={<App />} />}
      </Routes>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);