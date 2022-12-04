import React from "react";
import axios from "axios";
import { useState } from "react";
import { API_ROUTES, APP_ROUTES } from "../utils/constants";
import { Link, useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import InputGroup from "react-bootstrap/InputGroup";
import Row from "react-bootstrap/Row";
import { useEffect } from "react";

const CreateAuction = () => {
  const userId = "1";
  const [itemsForSale, setItemsForSale] = useState([]);
  const [validated, setValidated] = useState(false);

  const handleSubmit = (event) => {
    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    }
    event.preventDefault();
    setValidated(true);
  };

  useEffect(() => {
    const getItemsForSale = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5002/get_items_for_sale?user_id=" + userId
        );
        setItemsForSale(response.data.data);
        console.log(itemsForSale);
      } catch (error) {
        console.error(error);
      }
    };
    getItemsForSale();
  }, []);

  return (
    <Form noValidate validated={validated} onSubmit={handleSubmit}>
      <Col className="mb-3">
        <Form.Group as={Col} md="4" controlId="validationCustom01">
          <Form.Label>Item Name</Form.Label>
          <Form.Select aria-label="Default select example">
            {itemsForSale.map((item) => (
              <option key={item.id}>{item.name}</option>
            ))}
          </Form.Select>
        </Form.Group>
      </Col>
      <Button type="submit">Submit form</Button>
    </Form>
  );
};

export default CreateAuction;
