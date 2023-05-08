import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { ListProductsPage, GetAnalysisPage } from './pages';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<ListProductsPage />} />
      <Route path="/products" element={<ListProductsPage />} />
      <Route path="/analyses/:product_id" element={<GetAnalysisPage />} />
    </Routes>
  );
}

export default App;
