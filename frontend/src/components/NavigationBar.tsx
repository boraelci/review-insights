import React, { useState } from 'react';
import '../App.css';
import { Link } from 'react-router-dom';

export function NavigationBar() {
  return (
    <div className="masthead">
      <div className="masthead__section">
        <Link to="/">Review Insights</Link>
      </div>
    </div>
  );
}
