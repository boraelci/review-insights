import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import {
  CreateProductPage,
  ProductsPage,
  HomePage,
  AnalysesPage,
} from './pages';
import './App.css';

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/analyses/:product_id" element={<AnalysesPage />} />
        <Route path="/register" element={<CreateProductPage />} />
      </Routes>
    </div>
  );
}

export default App;
