import React, { useState } from 'react';
import '../App.css';
import { useNavigate } from 'react-router-dom';
import Masthead from '../components/Masthead.js';

export function HomePage() {
  const navigate = useNavigate();

  return (
    <div>
      {Masthead()}
      <div className="App">
        <h1>Review Insights</h1>
        <button onClick={() => navigate('/register')}>
          Register a product
        </button>
        <button onClick={() => navigate('/products')}>View products</button>
      </div>
    </div>
  );
}
