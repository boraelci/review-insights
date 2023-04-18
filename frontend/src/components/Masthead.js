import React, { useState } from 'react';
import '../App.css';

export function Masthead() {

  return (
    <div className="masthead">
      <div className="masthead__section">
        <a href="/">Home</a>
      </div>
      <div className="masthead__section">
        <a href="/register">New</a>
      </div>
      <div className="masthead__section">
        <a href="/products">View</a>
      </div>
      </div>
  );
}

export default Masthead;