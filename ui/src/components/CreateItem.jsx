import React, { useEffect } from "react";
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

const CreateItem = () => {
  const navigate = useNavigate();
  const [itemname, setItemname] = useState("");
  const [description, setDescription] = useState("");
  const [quantity, setQuantity] = useState(0);
  const [shipping, setShipping] = useState(0);
  const [isBuyNow, setIsBuyNow] = useState(true);
  const [price, setPrice] = useState(0);
  const [status, setStatus] = useState(0);
  const [categoryId, setCategoryId] = useState(0);
  const [validated, setValidated] = useState(false);
  const [user, setUser] = useState({});
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    getAuthenticatedUser().then((value) => setUser(value));
  }, []);

  const handleSubmit = (event) => {
    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    }
    event.preventDefault();
    console.log(itemname);
    setValidated(true);
    createItem();
  };

  const createItem = async () => {
    console.log(user);
    if (! user || !user["id"] || user["id"] === "") {
      alert("login before creating an item");
      return;
    }
    axios
      .post(
        "http://127.0.0.1:5002/create_item",
        {
          name: itemname,
          description: description,
          quantity: parseInt(quantity),
          shipping_cost: parseFloat(shipping),
          is_buy_now: isBuyNow === "true",
          price: parseFloat(price),
          category_id: categoryId,
          user_id: user["id"],
        },
        {
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            accept: "application/json",
          },
        }
      )
      .then((resp) => {
        if (resp.data.status) {
          alert("Item creation successful!");
          navigate(`/item/${resp.data.data.id}`, { state: { itemId: resp.data.data.id } });
        } else {
          alert("Item could not be created. Reason: " + resp.data.err_msg);
        }
        console.log(resp.data);
      });
  };

  const handleItemnameChange = (value) => {
    setItemname(value.target.value);
  };

  const handleDescriptionChange = (value) => {
    setDescription(value.target.value);
  };

  const handleQuantityChange = (value) => {
    setQuantity(value.target.value);
  };

  const handleShippingCostChange = (value) => {
    setShipping(value.target.value);
  };

  const handleIsBuyNowChange = (value) => {
    setIsBuyNow(value.target.value);
  };

  const handlePriceChange = (value) => {
    setPrice(value.target.value);
  };

  const handleCategoryIdChange = (value) => {
    setCategoryId(value.target.value);
  };

  const getAllCategories = async () => {
    axios.get("http://localhost:5001/get_all_categories").then(
      (response) => {
        console.log(response);
        if (response?.status != 200) {
          console.log("get all categories error");
          return;
        }
        console.log(response.data.data);
        let resp_categories = response.data.data;
        let categories_array = [];
        for (let i = 0; i < resp_categories.length; i++) {
          categories_array.push(
            <div key={resp_categories[i].id}>
              ID: {resp_categories[i].id} - Name: {resp_categories[i].name}
            </div>
          );
        }
        setCategories(categories_array);
      },
      (error) => {
        console.log(error);
      }
    );
  };


  return (
    <div>
      <Link to="/dashboard">Back to dashboard</Link>
      <div className="p-3 bg-light border">
                <h3>Get all categories</h3>
                <p>Use this category ID when you are creating items</p>
                <button
                    onClick={() => {
                        getAllCategories();
                    }}>
                    Get all the categories
                </button>
                <div>{categories}</div>
            </div>

      <Form noValidate validated={validated} onSubmit={handleSubmit}>
        <Col className="mb-3">
          <Form.Group as={Col} md="4" controlId="validationCustom01">
            <Form.Label>Item Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Item Name"
              required
              onChange={handleItemnameChange}
            />
          </Form.Group>
          <Form.Group as={Col} md="4" controlId="validationCustom02">
            <Form.Label>Description</Form.Label>
            <Form.Control
              type="text"
              placeholder="Description"
              onChange={handleDescriptionChange}
            />
          </Form.Group>
          <Form.Group as={Col} md="4" controlId="validationCustom03">
            <Form.Label>Quantity</Form.Label>
            <Form.Control type="number" placeholder="0" required onChange={handleQuantityChange} />
          </Form.Group>
          <Form.Group as={Col} md="4" controlId="validationCustom04">
            <Form.Label>Shipping Cost</Form.Label>
            <Form.Control
              type="number"
              placeholder="0"
              required
              onChange={handleShippingCostChange}
            />
          </Form.Group>
          <Form.Group as={Col} md="4" controlId="validationCustom05">
            <Form.Label>Price</Form.Label>
            <Form.Control type="number" placeholder="0" required onChange={handlePriceChange} />
          </Form.Group>
          <Form.Group as={Col} md="4" controlId="validationCustom06">
            <Form.Label>Is Buy Now</Form.Label>
            <Form.Control type="text" placeholder="true" onChange={handleIsBuyNowChange} />
          </Form.Group>
          <Form.Group as={Col} md="4" controlId="validationCustom07">
            <Form.Label>Category ID</Form.Label>
            <Form.Control
              type="number"
              placeholder="0"
              required
              onChange={handleCategoryIdChange}
            />
          </Form.Group>
        </Col>
        <Button type="submit">Submit form</Button>
      </Form>
      <div>
        <Link to="/saleitems">Back to Seller Page</Link>
      </div>
    </div>
  );
};

export default CreateItem;
