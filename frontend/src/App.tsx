import React, { useState } from 'react';
import Popup from 'reactjs-popup';
import {v4 as uuidv4} from 'uuid';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [link, setLink] = useState('');
  const [type, setType] = useState('');

  let status = ""
  const apiGatewayEndpoint = "https://s6bc2bia54.execute-api.us-east-1.amazonaws.com/test-stage";

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
    const id = uuidv4();

    // Call the API Gateway API with the product ID
    fetch(`${apiGatewayEndpoint}/products/${id}?name=${name}&link={link}&type=${type}`)
      .then(response => response.json())
      .then(data => {
        // Process the API response data
        console.log(data);
        status = "success"
      })
      .catch(error => {
        // Handle API error
        console.error(error);
        status = "failure"
      });
  };

  return (
    <div className="App">
      <header className="App-header">
          <h2>Enter Amazon Product Information:</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', justifyContent: 'center', textAlign: 'center' }}>
              <label>Product Name:</label>
              <input type="text" value={name} onChange={handleNameChange} placeholder="product name"/>

              <label>Product Link:</label>
              <input type="text" value={link} onChange={handleLinkChange} placeholder="link"/>

              <label>Product Category:</label>
              <input type="text" value={type} onChange={handleTypeChange} placeholder="category"/>

                <br></br>
              <button type="submit" style={{ marginRight: '10px' }}>Submit</button>
            </form>
      </header>
    </div>
  );
}

export default App;
