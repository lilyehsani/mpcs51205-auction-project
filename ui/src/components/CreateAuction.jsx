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
import { getAuthenticatedUser } from "../lib/common";
import { useEffect } from "react";

const CreateAuction = () => {
  const [user, setUser] = useState({});
  useEffect(() => {
    getAuthenticatedUser().then((value) => setUser(value));
  }, []);

  const navigate = useNavigate();
  const userId = "1";
  const [itemId, setItemId] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [startPrice, setStartPrice] = useState(-1);
  const [itemsForSale, setItemsForSale] = useState([]);
  const [validated, setValidated] = useState(false);

  const createAuction = async () => {
    try {
      console.log(parseInt(itemId), parseFloat(startPrice));
      const response = await axios.post(
        "http://127.0.0.1:5003/create_auction",
        {
          item_id: parseInt(itemId),
          start_time: startTime,
          end_time: endTime,
          start_price: parseFloat(startPrice),
        },
        {
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            accept: "application/json",
          },
        }
      );
      if (response.data.status) {
        alert("Auction creation successful!");
        navigate(`/item/${itemId}`, { state: { itemId: itemId } });
      } else {
        alert("Auction could not be created. Reason: " + response.data.err_msg);
        window.location.reload(false);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleSubmit = (e) => {
    const form = e.currentTarget;
    if (form.checkValidity() === false) {
      e.preventDefault();
      e.stopPropagation();
      alert("Form is incomplete.");
      return;
    }
    e.preventDefault();
    e.stopPropagation();
    var start = Date.parse(startTime);
    if (Number.isNaN(start)) {
      const err = "Incorrect start time format.";
      console.error(err);
      alert(err);
      return;
    }
    var end = Date.parse(endTime);
    if (Number.isNaN(end)) {
      const err = "Incorrect end time format.";
      console.error(err);
      alert(err);
      return;
    }
    createAuction(start, end);
    setValidated(true);
  };

  const handleItemSelect = (value) => {
    console.log(value.target.value);
    setItemId(value.target.value);
  };

  const handleStartTimeChange = (value) => {
    setStartTime(value.target.value);
  };

  const handleEndTimeChange = (value) => {
    setEndTime(value.target.value);
  };

  const handleStartPriceChange = (value) => {
    setStartPrice(value.target.value);
  };

  const getOptions = () => {
    if (itemsForSale.length === 1) {
      return;
    }
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
        <Form.Group as={Col} md="4">
          <Form.Label>Item Name</Form.Label>
          <Form.Select required onChange={handleItemSelect}>
            <option>Choose an existing item for sale.</option>
            {itemsForSale.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name}
              </option>
            ))}
          </Form.Select>
        </Form.Group>
        <Form.Group as={Col} md="4">
          <Form.Label>Start time (must be in YYYY-MM-DD HH:MM:SS format).</Form.Label>
          <Form.Control
            required
            type="text"
            placeholder="YYYY-MM-DD HH:MM:SS"
            onChange={handleStartTimeChange}
          />
        </Form.Group>
        <Form.Group as={Col} md="4">
          <Form.Label>End time (must be in YYYY-MM-DD HH:MM:SS format).</Form.Label>
          <Form.Control
            required
            type="text"
            placeholder="YYYY-MM-DD HH:MM:SS"
            onChange={handleEndTimeChange}
          />
        </Form.Group>
        <Form.Group as={Col} md="4">
          <Form.Label>Start price</Form.Label>
          <Form.Control required type="number" placeholder="0" onChange={handleStartPriceChange} />
        </Form.Group>
      </Col>
      <Button type="submit">Submit form</Button>
    </Form>
  );
};

export default CreateAuction;
