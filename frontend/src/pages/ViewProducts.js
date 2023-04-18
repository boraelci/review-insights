import React, { useState } from 'react';
import '../App.css';
import {apiGatewayEndpoint} from "../Constants.js"
import Masthead from "../components/Masthead.js"

export function ViewProducts() {

  return (
  <div>
  {Masthead()}
    <div className="App">
      <header className="App-header">
          <h2> List of all products will be displayed here</h2> </header>
    </div>
    </div>
  );
}

export default ViewProducts;