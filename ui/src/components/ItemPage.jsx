import React from "react";
import { useEffect, useState } from "react";
import { APP_ROUTES } from "../utils/constants";
import { useNavigate, useParams } from "react-router-dom";
import { useUser } from "../lib/customHooks";
import axios from "axios";
import "./index.css";

const ItemPage = () => {
  //   const navigate = useNavigate();
  //   const { user, authenticated } = useUser();
  //   if (!(user || authenticated)) {
  //     navigate(APP_ROUTES.SIGN_IN);
  //   }

  let { itemId } = useParams();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [isBuyNow, setIsBuyNow] = useState(false);
  const [buyNowPrice, setBuyNowPrice] = useState(-1);
  const [quantity, setQuantity] = useState(-1);
  const [shippingCost, setShippingCost] = useState("");

  const [auctions, setAuctions] = useState([]);

  const [itemLoading, setItemLoading] = useState(false);
  const [auctionLoading, setAuctionLoading] = useState(false);

  function numToPrice(num) {
    var strNum = num.toString();
    if (Number.isInteger(num)) {
      strNum += ".00";
    }
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
        console.error(error);
        setName("No item found.");
      } finally {
        setItemLoading(false);
      }
    };
    getItemInfo();
  }, [itemId]);

  useEffect(() => {
    const getAuctionInfo = async () => {
      setAuctionLoading(true);
      try {
        const auctionResponse = await axios.get(
          "http://127.0.0.1:5003/get_auctions_by_item_id?id=" + itemId
        );
        var data = auctionResponse.data.data;
        setAuctions(data);
        console.log(data.current_highest_bid_id);
      } catch (error) {
        console.error(error);
      } finally {
        setAuctionLoading(false);
      }
    };
    getAuctionInfo();
  }, [itemId]);

  return (
    <div>
      <h1>{name}</h1>
      {itemLoading && <div>Loading...</div>}
      <div>Description: {description}</div>
      <div>Category: {category}</div>
      <div>Quantity: {quantity}</div>
      <div>Shipping cost: {shippingCost}</div>
      {auctionLoading && <div>Loading...</div>}
      <div> Auctions:</div>
      {/* <div>Auctions: {renderAuctions()}</div> */}
      <table className="auctionTable">
        <tbody>
          <tr>
            <th>Current highest bid</th>
            <th>Start time</th>
            <th>End time</th>
          </tr>
          {auctions.map((auction) => (
            <tr key={auction.id}>
              <td className="auctionTd">
                {auction.current_highest_bid_id
                  ? getCurrentHighestBid(auction.current_highest_bid_id)
                  : "No bids yet"}
              </td>
              <td className="auctionTd">{auction.start_time}</td>
              <td className="auctionTd">{auction.end_time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ItemPage;
