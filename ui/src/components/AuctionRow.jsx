import React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import "./index.css";
import moment from "moment";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import { getAuthenticatedUser } from "../lib/common";

// Props: id (auction id), auction (auction)
const AuctionRow = (props) => {
  const [bidInput, setLastBid] = useState("");
  const [user, setUser] = useState({});

  useEffect(() => {
    getAuthenticatedUser().then((value) => {
      setUser(value);
    });
  }, []);

  const placeBid = async (bidAmount) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5003/place_bid",
        {
          auction_id: props.auction.id,
          user_id: user.id,
          bid_amount: bidAmount,
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

  function getDisplayTime(timeString) {
    //  return String(timeString);
    const relativeTime = moment(timeString).fromNow();
    var res = timeString + " (" + relativeTime + ")";
    return res;
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
              <Form.Control type="number" placeholder="0" required onChange={handleBidChange} />
              <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
            </Form.Group>
          </Col>
          <Button type="submit">Place Bid</Button>
        </Form>
        <div>
          This operation can take time and will alert you when it is complete. Please only press the
          button once.
        </div>
      </td>
      <td>{getDisplayTime(props.auction.start_time)}</td>
      <td>{getDisplayTime(props.auction.end_time)}</td>
    </tr>
  );
};

export default AuctionRow;
