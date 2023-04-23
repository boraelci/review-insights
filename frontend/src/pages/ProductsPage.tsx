import React, { useState } from 'react';
import '../App.css';
import Masthead from '../components/Masthead.js';

export function ProductsPage() {
  return (
    <div>
      {Masthead()}
      <div className="App">
        <header className="App-header">
          <h2> List of all products will be displayed here</h2>{' '}
        </header>
      </div>
    </div>
  );
}
