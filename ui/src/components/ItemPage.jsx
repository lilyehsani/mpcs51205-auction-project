import React from "react";
import { useEffect, useState } from "react";
import { APP_ROUTES } from "../utils/constants";
import { useNavigate, useParams } from "react-router-dom";
import { useUser } from "../lib/customHooks";
import axios from "axios";
import "./index.css";
import moment from "moment";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Table from "react-bootstrap/Table";
import AuctionRow from "./AuctionRow";
import { getAuthenticatedUser } from "../lib/common";

const ItemPage = () => {
  const [user, setUser] = useState({});
  // console.log(user);

  let { itemId } = useParams();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [isBuyNow, setIsBuyNow] = useState(-1);
  const [buyNowPrice, setBuyNowPrice] = useState(-1);
  const [quantityToBuy, setQuantityToBuy] = useState(-1);
  const [quantity, setQuantity] = useState(-1);
  const [shippingCost, setShippingCost] = useState("");

  const [auctions, setAuctions] = useState([]);

  const [itemLoading, setItemLoading] = useState(false);
  const [auctionsLoading, setAuctionsLoading] = useState(false);

  function numToPrice(num) {
    var strNum = num.toFixed(2);
    return "$" + strNum;
  }

  useEffect(() => {
    const getItemInfo = async () => {
      setItemLoading(true);
      try {
        const response = await axios.get("http://127.0.0.1:5001/get_items?ids=" + itemId);
        var data = response.data.data[0];
        setName(data.name);
        setDescription(data.description);
        setCategory(data.category);
        setIsBuyNow(data.is_buy_now);
        setBuyNowPrice(data.price);
        setQuantity(data.quantity);
        setShippingCost(numToPrice(data.shipping_cost));
      } catch (error) {
        if (error instanceof TypeError) {
          setName("No item found.");
        } else {
          setName("Unable to connect to backend.");
        }
      } finally {
        setItemLoading(false);
      }
    };
    getItemInfo();
  }, [itemId]);

  useEffect(() => {
    const getAuctionInfo = async () => {
      setAuctionsLoading(true);
      try {
        const auctionResponse = await axios.get(
          "http://127.0.0.1:5003/get_auctions_by_item_id?id=" + itemId
        );
        var data = auctionResponse.data.data;
        setAuctions(data);
      } catch (error) {
        console.error(error);
      } finally {
        setAuctionsLoading(false);
      }
    };
    getAuctionInfo();
  }, [itemId]);

  useEffect(() => {
    getAuthenticatedUser().then((value) => setUser(value));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    e.stopPropagation();
    // todo: add to card
  };

  const handleQuantityToBuyChange = (value) => {
    setQuantityToBuy(value.target.value);
  };

  return (
    <div>
      <h1>Name: {name}</h1>
      {itemLoading && <div>Loading...</div>}
      <div>Description: {description}</div>
      <div>Category: {category}</div>
      <div>Quantity: {quantity}</div>
      <div>Shipping cost: {shippingCost}</div>
      <div>
        {isBuyNow === 1 && (
          <Form noValidate onSubmit={handleSubmit}>
            <Col className="mb-3">
              <Form.Group as={Col} md="4">
                <Form.Label>Quantity to buy:</Form.Label>
                <Form.Control
                  required
                  type="number"
                  placeholder="0"
                  onChange={handleQuantityToBuyChange}
                />
              </Form.Group>
            </Col>
            <Button type="submit">Submit form</Button>
          </Form>
        )}
      </div>
      {auctionsLoading && <div>Loading...</div>}
      <h2>Auctions:</h2>
      <Table striped bordered>
        <tbody>
          <tr>
            <th>Status</th>
            <th>Starting price</th>
            <th>Current highest bid</th>
            <th>Place bid</th>
            <th>Start time</th>
            <th>End time (Refresh page for up-to-date times)</th>
          </tr>
          {auctions.map((auction) => (
            <AuctionRow key={auction.id} auction={auction} />
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default ItemPage;
