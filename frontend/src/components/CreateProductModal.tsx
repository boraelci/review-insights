import React, { useState } from 'react';
import '../App.css';
import { API_GATEWAY_ENDPOINT } from '../Config';
import { NavigationBar } from '.';
import { Container, Row, Col, Form, Button, Modal } from 'react-bootstrap';

interface CreateProductModalProps {
  showModal: boolean;
  handleClose: () => void;
}

export const CreateProductModal: React.FC<CreateProductModalProps> = ({
  showModal,
  handleClose,
}) => {
  const [name, setName] = useState('');
  const [link, setLink] = useState('');
  const [category, setCategory] = useState('');
  const [email, setEmail] = useState('');

  let status = '';

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    // Call the API Gateway API with the product ID
    fetch(`${API_GATEWAY_ENDPOINT}/products`, {
      method: 'POST',
      body: JSON.stringify({
        product_name: name,
        product_link: link,
        product_category: category,
        seller_id: email,
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
    handleClose();
  };
  return (
    <Modal show={showModal} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Add Product</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="productName">
            <Form.Label>Name:</Form.Label>
            <Form.Control
              type="text"
              value={name}
              onChange={(event: any) => setName(event.target.value)}
              placeholder="Apple AirPods Pro (2nd Generation) Wireless Earbuds, Up to 2X More Active Noise Cancelling, Adaptive Transparency, Personalized Spatial Audio, MagSafe Charging Case, Bluetooth Headphones for iPhone"
            />
          </Form.Group>

          <Form.Group controlId="productLink" className="mt-3">
            <Form.Label>Link:</Form.Label>
            <Form.Control
              type="text"
              value={link}
              onChange={(event: any) => setLink(event.target.value)}
              placeholder="https://www.amazon.com/Apple-Generation-Cancelling-Transparency-Personalized/dp/B0BDHWDR12"
            />
          </Form.Group>

          <Form.Group controlId="productCategory" className="mt-3">
            <Form.Label>Category:</Form.Label>
            <Form.Control
              type="text"
              value={category}
              onChange={(event: any) => setCategory(event.target.value)}
              placeholder="Headphones"
            />
          </Form.Group>

          <Form.Group controlId="email" className="mt-3">
            <Form.Label>E-mail:</Form.Label>
            <Form.Control
              type="text"
              value={email}
              onChange={(event: any) => setEmail(event.target.value)}
              placeholder="be2246@columbia.edu"
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleSubmit}>
          Submit
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
