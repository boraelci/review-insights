import React, { useState, useEffect } from 'react';
import '../App.css';
import Masthead from '../components/Masthead.js';
import { useParams } from 'react-router-dom';
import { API_GATEWAY_ENDPOINT } from '../Config';

import { HistoricalView } from '../components';

export function AnalysesPage() {
  const { product_id } = useParams();
  console.log(product_id);

  // https://eref68msii.execute-api.us-east-1.amazonaws.com/prod/analyses/cd63df10-22ab-4bc3-9dd8-0c908555c31a
  // Call the API Gateway API with the product ID
  // Add these states
  const [positiveData, setPositiveData] = useState<
    { date: string; count: number }[]
  >([]);
  const [negativeData, setNegativeData] = useState<
    { date: string; count: number }[]
  >([]);

  useEffect(() => {
    fetch(`${API_GATEWAY_ENDPOINT}/analyses/${product_id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        console.log(data.body.historical_data);
        // Store the data in the states
        setPositiveData(data.body.historical_data.positive);
        setNegativeData(data.body.historical_data.negative);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  // Pass the data to the HistoricalView component
  return (
    <div style={{ width: '85%' }}>
      {positiveData.length > 0 && negativeData.length > 0 ? (
        <HistoricalView
          positiveData={positiveData}
          negativeData={negativeData}
        />
      ) : (
        <p>Loading data...</p>
      )}
    </div>
  );
}
