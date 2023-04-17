import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import {v4 as uuidv4} from 'uuid';
import {
  Home
} from "./pages/Home.js";
import './App.css';

function App() {

  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />}/>
      </Routes>
    </div>
  );
}

export default App;