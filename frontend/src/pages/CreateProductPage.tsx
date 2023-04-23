import React, { useState } from 'react';
import '../App.css';
import { API_GATEWAY_ENDPOINT } from '../Config';
import Masthead from '../components/Masthead.js';

export function CreateProductPage() {
  const [name, setName] = useState('');
  const [link, setLink] = useState('');
  const [type, setType] = useState('');

  let status = '';

  const handleNameChange = (event: any) => {
    setName(event.target.value);
  };

  const handleLinkChange = (event: any) => {
    setLink(event.target.value);
  };

  const handleTypeChange = (event: any) => {
    setType(event.target.value);
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    // Call the API Gateway API with the product ID
    fetch(`${API_GATEWAY_ENDPOINT}/products`, {
      method: 'POST',
      body: JSON.stringify({
        product_name: name,
        product_link: link,
        product_category: type,
      }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Process the API response data
        console.log(data);
        status = 'success';
      })
      .catch((error) => {
        // Handle API error
        console.error(error);
        status = 'failure';
      });
  };

  return (
    <div>
      {Masthead()}
      <div className="App">
        <header className="Register-header">
          <h2>Enter Amazon Product Information:</h2>
          <form
            onSubmit={handleSubmit}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'flex-start',
              justifyContent: 'center',
              textAlign: 'center',
            }}
          >
            <label>Product Name:</label>
            <input
              type="text"
              value={name}
              onChange={handleNameChange}
              placeholder="product name"
            />

            <label>Product Link:</label>
            <input
              type="text"
              value={link}
              onChange={handleLinkChange}
              placeholder="link"
            />

            <label>Product Category:</label>
            <input
              type="text"
              value={type}
              onChange={handleTypeChange}
              placeholder="category"
            />

            <br></br>
            <button type="submit" style={{ marginRight: '10px' }}>
              Submit
            </button>
          </form>
        </header>
      </div>
    </div>
  );
}
