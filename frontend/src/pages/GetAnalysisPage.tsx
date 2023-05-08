import React, { useState, useEffect } from 'react';
import '../App.css';
import {
  HistoricalDataModel,
  NavigationBar,
  CategoricalDataModel,
} from '../components';
import { useParams } from 'react-router-dom';
import { API_GATEWAY_ENDPOINT } from '../Config';

import { HistoricalView, CategoricalView } from '../components';
import { Button, Col, Container, Row } from 'react-bootstrap';

export function GetAnalysisPage() {
  let { product_id } = useParams();

  if (product_id === '1') {
    product_id = 'cd63df10-22ab-4bc3-9dd8-0c908555c31a';
  }

  console.log(product_id);

  // https://eref68msii.execute-api.us-east-1.amazonaws.com/prod/analyses/cd63df10-22ab-4bc3-9dd8-0c908555c31a
  // Call the API Gateway API with the product ID
  // Add these states
  const [historicalPositives, setHistoricalPositives] = useState<Record<
    string,
    number
  > | null>(null);
  const [historicalNegatives, setHistoricalNegatives] = useState<Record<
    string,
    number
  > | null>(null);

  const [categoricalPositives, setCategoricalPositives] = useState<Record<
    string,
    number
  > | null>(null);
  const [categoricalNegatives, setCategoricalNegatives] = useState<Record<
    string,
    number
  > | null>(null);

  useEffect(() => {
    fetch(`${API_GATEWAY_ENDPOINT}/analyses/${product_id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((r) => r.json())
      .then((response) => {
        console.log(response);
        if (response.statusCode === 200) {
          // console.log(response.body.historical_data);
          // Store the data in the states
          setHistoricalPositives(response.body.historical_data.positives);
          setHistoricalNegatives(response.body.historical_data.negatives);

          setCategoricalPositives(response.body.categorical_data.positives);
          setCategoricalNegatives(response.body.categorical_data.negatives);
        }
      })
      .catch((error) => {
        console.error(error);
      });
    // getDataFromLocal();
  }, [product_id]);

  // Pass the data to the HistoricalView component
  return (
    <div>
      <NavigationBar />
      <Container>
        <Row>
          <Col className="col-2"></Col>
          <Col className="col-8">
            <div className="card h-100 shadow p-3">
              <div className="card-body">
                {historicalPositives && historicalNegatives ? (
                  <HistoricalView
                    historicalDataModel={
                      new HistoricalDataModel({
                        positives: historicalPositives,
                        negatives: historicalNegatives,
                      })
                    }
                  />
                ) : (
                  <div>
                    <p>Loading data... </p>
                  </div>
                )}
              </div>
            </div>
          </Col>
          <Col className="col-2"></Col>
        </Row>
        <Row>
          <Col className="col-3"></Col>
          <Col className="col-6">
            <div className="card h-100 shadow p-3">
              <div className="card-body">
                {categoricalPositives && categoricalNegatives ? (
                  <CategoricalView
                    categoricalDataModel={
                      new CategoricalDataModel({
                        positives: categoricalPositives,
                        negatives: categoricalNegatives,
                      })
                    }
                  />
                ) : (
                  <div>
                    <p>Loading data... </p>
                  </div>
                )}
              </div>
            </div>
          </Col>
          <Col className="col-3"></Col>
        </Row>
      </Container>
    </div>
  );
}
