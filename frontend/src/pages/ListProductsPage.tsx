import React, { useEffect, useState } from 'react';
import '../App.css';
import { NavigationBar, CreateProductModal } from '../components';
import {
  Button,
  Col,
  Container,
  Form,
  FormControl,
  Row,
} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';
import { API_GATEWAY_ENDPOINT } from '../Config';

interface Product {
  product_id: string;
  product_name: string;
  product_link: string;
  product_category: string;
  analysis_status: string;
}

interface ProductItemProps {
  product: Product;
}

const ProductItem: React.FC<ProductItemProps> = ({ product }) => {
  const getColor = (status: string): string => {
    if (status === 'Failed') {
      return 'text-danger fw-bold';
    } else if (status === 'Pending') {
      return 'text-warning fw-bold';
    } else if (status === 'Ready') {
      return 'text-success fw-bold';
    } else {
      return '';
    }
  };

  return (
    <div className="col-md-4 mb-3">
      <Link
        to={`/analyses/${product.product_id}`}
        style={{ textDecoration: 'none', color: 'inherit' }}
      >
        <div className="card h-100 shadow p-3">
          <div className="card-body">
            <h4 className="card-title">{product.product_name}</h4>
            <p className="card-text link-text">{product.product_link}</p>
            <p className="card-text">{product.product_category}</p>
            <p className={`${getColor(product.analysis_status)}`}>
              {product.analysis_status}
            </p>
          </div>
        </div>
      </Link>
    </div>
  );
};

interface ProductsProps {
  products: Product[];
}

const Products: React.FC<ProductsProps> = ({ products }) => {
  return (
    <div className="container">
      <h2 className="text-center mb-4">Products</h2>
      <div className="text-center mb-4"></div>
      <div className="row">
        {products.map((product) => (
          <ProductItem key={product.product_id} product={product} />
        ))}
      </div>
    </div>
  );
};

export function ListProductsPage() {
  const [showModal, setShowModal] = useState(false);

  const handleClose = () => setShowModal(false);
  const handleShow = () => setShowModal(true);

  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetch(`${API_GATEWAY_ENDPOINT}/products`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((r) => r.json())
      .then((response) => {
        console.log(response);
        if (response.statusCode === 200) {
          // Store the list of products in the state
          setProducts(response.body);
        }
      })
      .catch((error) => {
        console.error(error);
      });
    // getDataFromLocal();
  }, []);

  const [searchTerm, setSearchTerm] = useState('');
  const [filteredProducts, setFilteredProducts] = useState<Product[]>(products);

  useEffect(() => {
    setFilteredProducts(
      products.filter((product) =>
        product.product_name.toLowerCase().includes(searchTerm.toLowerCase()),
      ),
    );
  }, [searchTerm, products]);

  return (
    <div>
      <NavigationBar />
      <CreateProductModal showModal={showModal} handleClose={handleClose} />
      <Container>
        <div className="text-center mb-4 mt-4">
          <button
            className="btn btn-circle btn-lg btn-outline-dark"
            onClick={handleShow}
          >
            Add <FontAwesomeIcon icon={faPlus} />
          </button>
        </div>
        <Row>
          <Col>
            <Form>
              <FormControl
                type="text"
                placeholder="Search by product name"
                className="mr-sm-2"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </Form>
          </Col>
        </Row>
        <br></br>
        <Row>
          {filteredProducts.map((product) => (
            <ProductItem key={product.product_id} product={product} />
          ))}
        </Row>
      </Container>
    </div>
  );
}
