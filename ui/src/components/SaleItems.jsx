import {useEffect, useState} from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import {getAuthenticatedUser} from "../lib/common";

const SaleItems = () => {
    const [items, setItems] = useState([]);
    const [data, setData] = useState({});
    const [user, setUser] = useState({});

    useEffect(() => {
        getAuthenticatedUser().then((value) => setUser(value));
    }, []);

    const updateItemForSale = (event) => {
        const form = event.currentTarget;
        event.preventDefault();
        console.log(data);
        axios.post("http://127.0.0.1:5001/update_item", data, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type':  'application/json',
                'accept': "application/json",
            }
        }).then(resp => console.log(resp.data))
    }

    const handleItemIdChange = (value) => {
        data["id"] = parseInt(value.target.value);
        // data.push({
        //     key: "id",
        //     value: parseInt(value.target.value)
        // });
    }

    const handleItemnameChange = (value) => {
        data["name"] = value.target.value;
        // data.push({
        //     key: "name",
        //     value: value.target.value
        // });
    }

    const handleDescriptionChange = (value) => {
        data["description"] = value.target.value;
        // data.push({
        //     key: "description",
        //     value: value.target.value
        // });
    }

    const handleQuantityChange = (value) => {
        data["quantity"] = parseInt(value.target.value);
        // data.push({
        //     key: "quantity",
        //     value: parseInt(value.target.value)
        // });
    }

    const handleShippingCostChange = (value) => {
        data["shipping_cost"] = parseFloat(value.target.value);
        // data.push({
        //     key: "shipping_cost",
        //     value: parseFloat(value.target.value)
        // });
    }

    const handleIsBuyNowChange = (value) => {
        data["is_buy_now"] = (value.target.value === true)
        // data.push({
        //     key: "is_buy_now",
        //     value: (value.target.value === true)
        // });
    }

    const handlePriceChange = (value) => {
        data["price"] = parseFloat(value.target.value);
        // data.push({
        //     key: "price",
        //     value: parseFloat(value.target.value)
        // });
    }

    const handleCategoryIdChange = (value) => {
        data["category_id"] = parseInt(value.target.value);
        // data.push({
        //     key: "category_id",
        //     value: parseInt(value.target.value)
        // });
    }

    const removeItemForSale = async (itemID) => {
        axios.post("http://127.0.0.1:5002/remove_item_for_sale", {
            user_id: user['id'],
            item_id: parseInt(itemID),
        }, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'accept': "application/json",
            }
        })
            .then((response) => {
                console.log(response);
                if (response?.status != 200) {
                    console.log("remove_item_for_sale error");
                    return;
                }
                if (!response?.data?.status) {
                    alert(response?.data?.err_msg);
                    return;
                }
                alert("click the refresh button to see the result");
                return;
            }, (error) => {
                console.log(error);
            });        
    }

    const getSaleItems = async () => {
        axios.get("http://localhost:5002/get_items_for_sale?user_id=" + user['id'])
            .then((response) => {
                console.log(response);
                if (response?.status != 200) {
                    console.log("get_items_for_sale error");
                    return;
                }
                if (!response.data.status) {
                    console.log(response.data);
                    return;
                }
                let resp_items = response.data.data;
                if (resp_items === null) {
                    setItems([]);
                    // alert("no items found");
                    return;
                }
                let array = [];
                for (let i = 0; i < resp_items.length; i++) {
                    let cur_url = "/item/" + resp_items[i].id;
                    array.push(
                        <div key={resp_items[i].id}>
                            <div>{resp_items[i].id} - {resp_items[i].name} - {resp_items[i].description}</div>
                            <Link to={cur_url}>see details</Link>
                            <button onClick={() => {removeItemForSale(resp_items[i].id);}}>Delete it</button>
                        </div>

                    );
                }
                setItems(array);
            }, (error) => {
                console.log(error);
            });
    };

    return (
        <div>
            <div>Your items currently selling</div>
            <div className="p-5 bg-light border">
            <button onClick={() => { (getSaleItems()) }}>Refresh</button>
            <div>Click to refresh and see your items on sale. (Empty if no items are on sale)</div>
                <div className="p-3 bg-light border">
                {items}
                </div>  
            </div>
            <div>Update item information here!</div>
            <Form onSubmit={updateItemForSale}>
                <Col className="mb-3">
                    <Form.Group as={Col} md="4" controlId="validationCustom01">
                        <Form.Label>Item ID</Form.Label>
                        <Form.Control
                            type="number"
                            placeholder="0"
                            onChange={handleItemIdChange}
                        />
                    </Form.Group>
                    <Form.Group as={Col} md="4" controlId="validationCustom01">
                        <Form.Label>Item Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Item Name"
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
                            onChange={handleQuantityChange}
                        />
                    </Form.Group>
                    <Form.Group as={Col} md="4" controlId="validationCustom04">
                        <Form.Label>Shipping Cost</Form.Label>
                        <Form.Control
                            type="number"
                            placeholder="0"
                            onChange={handleShippingCostChange}
                        />
                    </Form.Group>
                    <Form.Group as={Col} md="4" controlId="validationCustom05">
                        <Form.Label>Price</Form.Label>
                        <Form.Control
                            type="number"
                            placeholder="0"
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
                            onChange={handleCategoryIdChange}
                        />
                    </Form.Group>
                </Col>
                <Button type="submit">Submit change</Button>
            </Form>
            <div>
                <Link to="/createitem">Create an item</Link>
            </div>
            <div>
                <Link to="/dashboard">Back to dashboard</Link>
            </div>
        </div>
    );
}

export default SaleItems;