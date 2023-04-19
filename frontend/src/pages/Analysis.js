import React, { useState } from 'react';
import '../App.css';
import Masthead from "../components/Masthead.js"
import { useParams } from 'react-router-dom';
import {API_GATEWAY_ENDPOINT} from "../Config.tsx"

export function Analysis() {
  const { id } = useParams();
  const product_id = id["id"]
  console.log(product_id)

    // Call the API Gateway API with the product ID
    fetch(`${API_GATEWAY_ENDPOINT}/analysis`, {
      method: "POST",
      body: JSON.stringify({
        "id": id}),
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(response => response.json())
      .then(data => {
        // Process the API response data
        console.log(data);
      })
      .catch(error => {
        // Handle API error
        console.error(error);
      });

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