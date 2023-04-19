import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import {Register} from "./pages/Register.js";
import {Home} from "./pages/Home.js";
import {Analysis} from "./pages/Analysis.js";
import {ViewProducts} from "./pages/ViewProducts.js"
import './App.css';

function App() {

  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/products" element={<ViewProducts />}/>
        <Route path="/analysis/:id" element={<Analysis />}/>
        <Route path="/register" element={<Register />}/>
      </Routes>
    </div>
  );
}

export default App;