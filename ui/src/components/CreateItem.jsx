import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import { API_ROUTES, APP_ROUTES } from '../utils/constants';
import { Link, useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import InputGroup from 'react-bootstrap/InputGroup';
import Row from 'react-bootstrap/Row';

const CreateItem = () => {
    const navigate = useNavigate()
    const [itemname, setItemname] = useState('');
    const [description, setDescription] = useState('');
    const [quantity, setQuantity] = useState(0);
    const [shipping, setShipping] = useState(0);
    const [isBuyNow, setIsBuyNow] = useState(true);
    const [price, setPrice] = useState(0);
    const [status, setStatus] = useState(0);
    const [categoryId, setCategoryId] = useState(0);
    const [validated, setValidated] = useState(false);

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
        try {
            const response = await axios({
                method: 'POST',
                url: "http://127.0.0.1:5001/create_item/",
                // inventory_input = {'name': data.get('name'), 'description': data.get('description'), 'quantity' : data.get('quantity'), 'shipping_cost' :data.get('shipping_cost'), 'is_buy_now' : data.get('is_buy_now'), 'price' : data.get('price'), 'category_id': data.get('category_id')}
                data: {
                    'name': itemname,
                    'description': description,
                    'quantity': quantity,
                    'shipping_cost': shipping,
                    'is_buy_now': isBuyNow,
                    'price': price,
                    'category_id': categoryId,
                    'user_id': 1
                }
                // todo: get user_id in session
            });
            if (!response?.data?.token) {
                console.log('Something went wrong during creating item: ', response);
                return;
            }
            console.log(response)
            // todo: navigate to seller page after creating items
            // navigate(APP_ROUTES.SELLER);
        }
        catch (err) {
            console.log('Some error occurred during creating item: ', err);
        }
    };

    const handleItemnameChange = (value) => {
        setItemname(value.target.value);
    }

    const handleDescriptionChange = (value) => {
        setDescription(value.target.value);
    }

    const handleQuantityChange = (value) => {
        setQuantity(value.target.value);
    }

    const handleShippingCostChange = (value) => {
        setShipping(value.target.value);
    }

    const handleIsBuyNowChange = (value) => {
        setIsBuyNow(value.target.value);
    }

    const handlePriceChange = (value) => {
        setPrice(value.target.value);
    }

    const handleCategoryIdChange = (value) => {
        setCategoryId(value.target.value);
    }

    return (
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
                    <Form.Control
                        type="number"
                        placeholder="0"
                        required
                        onChange={handleQuantityChange}
                    />
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
                    <Form.Control
                        type="number"
                        placeholder="0"
                        required
                        onChange={handlePriceChange}
                    />
                </Form.Group>
                <Form.Group as={Col} md="4" controlId="validationCustom06">
                    <Form.Label>Is Buy Now</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="true"
                        onChange={handleIsBuyNowChange}
                    />
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
    );
}

export default CreateItem;