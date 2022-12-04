import React from "react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useUser } from "../lib/customHooks";
import axios from "axios";

const ItemPage = () => {
  const navigate = useNavigate();
  const { user, authenticated } = useUser();
  if (!(user || authenticated)) {
    navigate(APP_ROUTES.SIGN_IN);
  }

  let { itemId } = useParams();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [isBuyNow, setIsBuyNow] = useState(false);
  const [buyNowPrice, setBuyNowPrice] = useState(-1);
  const [quantity, setQuantity] = useState(-1);
  const [shippingCost, setShippingCost] = useState("");

  const [itemLoading, setItemLoading] = useState(false);

  function numToPrice(num) {
    var strNum = num.toString();
    if (Number.isInteger(num)) {
      strNum += ".00";
    }
    return "$" + strNum;
  }

  function setFields(data) {
    setName(data.name);
    setDescription(data.description);
    setCategory(data.category);
    setIsBuyNow(data.is_buy_now);
    setBuyNowPrice(data.price);
    setQuantity(data.quantity);
    setShippingCost(numToPrice(data.shipping_cost));
  }

  useEffect(() => {
    const getItemInfo = async () => {
      setItemLoading(true);
      try {
        const response = await axios.get("http://127.0.0.1:5001/get_items?ids=" + itemId);
        console.log(response);
        console.log(response.data.data[0].shipping_cost);
        setFields(response.data.data[0]);
      } catch (error) {
        console.error(error);
        setName("No name found.");
      } finally {
        setItemLoading(false);
      }
    };
    getItemInfo();
  }, [itemId]);

  return (
    <div>
      <h1>{name}</h1>
      {itemLoading && <div>Loading...</div>}
      <div>Description: {description}</div>
      <div>Category: {category}</div>
      <div>Quantity: {quantity}</div>
      <div>Shipping cost: {shippingCost}</div>
    </div>
  );
};

export default ItemPage;
