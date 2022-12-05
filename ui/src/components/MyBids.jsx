import React from "react";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import { getAuthenticatedUser } from "../lib/common";
import { useEffect } from "react";
import { Link } from "react-router-dom";
import Table from "react-bootstrap/Table";

const MyBids = () => {
  const [user, setUser] = useState({});
  const [userLoading, setUserLoading] = useState(false);
  const navigate = useNavigate();
  const [bids, setBids] = useState([]);

  useEffect(() => {
    getAuthenticatedUser().then((value) => setUser(value));
  }, []);

  const getBids = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5003/get_bids_by_user?id=" + user.id);
      setBids(response.data.data);
      console.log(bids);
    } catch (error) {
      console.error(error);
    }
  };

  const handleGetBids = (event) => {
    event.preventDefault();
    event.stopPropagation();
    getBids();
  };

  return (
    <div>
      <Link to="/dashboard">Back to dashboard</Link>
      <div>
        <Button type="button" onClick={handleGetBids}>
          Get my bids
        </Button>
        {bids.length === 0 || bids === null ? (
          <div>No bids found</div>
        ) : (
          <Table striped bordered>
            <tbody>
              <tr>
                <th>Bid amount</th>
                <th>Bid time</th>
                <th>Item</th>
              </tr>
              {bids.map((bid) => (
                <tr key={bid.id}>
                  <td>{bid.bid_amount}</td>
                  <td>{bid.bid_time}</td>
                  <td>
                    <Link to={"/item/" + bid.item_id}>Details</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        )}
      </div>
    </div>
  );
};

export default MyBids;
