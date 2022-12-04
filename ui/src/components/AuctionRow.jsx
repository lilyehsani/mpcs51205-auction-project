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

// Props: id (auction id), auction (auction)
const AuctionRow = (props) => {
  //   const navigate = useNavigate();
  //   const { user, authenticated } = useUser();
  //   if (!(user || authenticated)) {
  //     navigate(APP_ROUTES.SIGN_IN);
  //   }
  const [bidInput, setLastBid] = useState("");

  const placeBid = async (bidAmount) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5003/place_bid",
        {
          auction_id: props.auction.id,
          user_id: "1",
          bid_amount: bidAmount,
          // todo: get user_id in session
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
        alert("Bid successful!");
        window.location.reload(false);
      } else {
        alert("Bid could not be placed. Reason: " + response.data.err_msg);
        window.location.reload(false);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handlePlaceBid = (e) => {
    e.preventDefault();
    e.stopPropagation();
    var bid = Number(bidInput);
    if (Number.isNaN(bid)) {
      const err = "Bid must be a number.";
      console.error(err);
      alert(err);
    } else {
      // Parse as a price
      const bidStr = bid.toFixed(2);
      const bidNum = parseFloat(bidStr);
      placeBid(bidNum);
    }
  };

  function getRelativeTime(timeString) {
    return moment(timeString).fromNow();
  }

  function numToPrice(num) {
    var strNum = num.toFixed(2);
    return "$" + strNum;
  }

  function getAuctionStatus(status) {
    switch (status) {
      case 0:
        return "Not yet started";
      case 1:
        return "In progress";
      default:
        return "Ended";
    }
  }

  const handleBidChange = (value) => {
    setLastBid(value.target.value);
    console.log(value.target.value);
  };

  return (
    <tr key={props.auction.id}>
      <td>{getAuctionStatus(props.auction.status)}</td>
      <td>{numToPrice(props.auction.start_price)}</td>
      <td>
        {props.auction.current_highest_bid_amount
          ? numToPrice(props.auction.current_highest_bid_amount)
          : "No bids yet"}
      </td>
      <td>
        <Form noValidate onSubmit={handlePlaceBid}>
          <Col>
            <Form.Group as={Col} md="4" controlId="validationCustom01">
              <Form.Control type="text" placeholder="Bid" required onChange={handleBidChange} />
              <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
            </Form.Group>
          </Col>
          <Button type="submit">Place Bid</Button>
        </Form>
      </td>
      <td>{getRelativeTime(props.auction.start_time)}</td>
      <td>{getRelativeTime(props.auction.end_time)}</td>
    </tr>
  );
};

export default AuctionRow;
