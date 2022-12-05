import React, {useEffect} from 'react';
import axios from 'axios';
import { useState } from 'react';
import { API_ROUTES, APP_ROUTES } from '../utils/constants';
import { Link, useNavigate } from 'react-router-dom';
import {getAuthenticatedUser} from "../lib/common";

const Cart = () => {
    const [userid, setUserId] = useState(1);
    const [items, setItems] = useState([]);
    const [user, setUser] = useState({});

    useEffect(() => {
        getAuthenticatedUser().then((value) => setUser(value));
        setUserId(user['id']);
    }, []);

    const deleteItemInCart = async (itemId) => {
        const response = await axios.delete("http://127.0.0.1:5002/remove_item_from_cart?id=" + userid + "&item=" + itemId);
        console.log(response);
        window.location.reload();
    }

    useEffect(() => {
        const getItemsInCart = async () => {
            // todo: replace user id in url
            const response = await axios.get("http://127.0.0.1:5002/get_items_in_cart?id=" + userid, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type':  'application/json',
                    'accept': "application/json",
                }
            });
            console.log(response.data.data);
            var resp_items = response.data.data;
            console.log(resp_items.length);
            console.log(resp_items[0]);
            setItems(resp_items);
            //console.log(items);
        };
        getItemsInCart();
    }, []);

    return (
            <div  className="p-5 bg-light border">
                <h1>Shopping Cart</h1>
                <ul>
                    {items.map((item) => (
                        <li key={item.id}>
                            <span>{"ID: " + item.id + ", Name: "}</span>
                            <span>{item.name + ",  Description: "}</span>
                            <span>{item.description + ",  Price: "}</span>
                            <span>{item.price}</span>
                            <span> </span>
                            <button onClick={() => { (deleteItemInCart(item.id)) }}>Delete</button>
                        </li>
                    ))}
                </ul>
            </div>
    );
}

export default Cart;