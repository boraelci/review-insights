import React, { useState } from 'react';
import '../App.css';
import Masthead from "../components/Masthead.js"

export function Analysis() {

  return (
  <div>
  {Masthead()}
    <div className="App">
      <header className="App-header">
          <h2> Graphs for a specific product will be displayed here</h2> </header>
    </div>
    </div>
  );
}

export default Analysis;