import React from "react";
import { useEffect, useState } from "react";
import { APP_ROUTES } from "../utils/constants";
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
import { Link, useNavigate } from "react-router-dom";

const AdminPage = () => {
  const [user, setUser] = useState({});
  const [validated, setValidated] = useState(false);
  const [selectedUserId, setSelectedUserId] = useState("");

  useEffect(() => {
    getAuthenticatedUser().then((value) => setUser(value));
  }, []);

  const [emails, setEmails] = useState([]);
  const [emailsLoading, setEmailsLoading] = useState(false);

  useEffect(() => {
    const getEmails = async () => {
      setEmailsLoading(true);
      try {
        const response = await axios.get("http://127.0.0.1:5006/get_all_email");
        // console.log(response);
        setEmails(response.data.data);
      } catch (error) {
        console.error(error);
      } finally {
        setEmailsLoading(false);
      }
    };
    getEmails();
  }, []);

  const [flaggedItems, setFlaggedItems] = useState([]);
  const [flaggedItemsLoading, setFlaggedItemsLoading] = useState(false);

  //   useEffect(() => {
  //     const getFlaggedItems = async () => {
  //       setFlaggedItemsLoading(true);
  //       try {
  //         const response = await axios.get("http://127.0.0.1:5001/get_red_flag_item");
  //         console.log(response);
  //       } catch (error) {
  //         console.error(error);
  //       } finally {
  //         setFlaggedItemsLoading(false);
  //       }
  //     };
  //     getFlaggedItems();
  //   }, []);

  useEffect(() => {
    const getFlaggedItems = async () => {
      setFlaggedItemsLoading(true);
      try {
        const response = await axios.get("http://127.0.0.1:5001/get_red_flag_item");
        // console.log(response);
        setFlaggedItems(response.data.data);
      } catch (error) {
        console.error(error);
      } finally {
        setFlaggedItemsLoading(false);
      }
    };
    getFlaggedItems();
  }, []);

  const handleSubmit = (event) => {
    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    }
    setValidated(true);

    axios
      .put("http://127.0.0.1:5005/account/suspend/" + selectedUserId, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json",
          accept: "application/json",
        },
      })
      .then((resp) => console.log(resp.data));

    event.preventDefault();
    event.stopPropagation();
  };

  const handleUserIdChange = (value) => {
    setSelectedUserId(value.target.value);
  };

  if (user.user_name === "admin") {
    return (
      <div>
        <Link to="/dashboard">Back to dashboard</Link>
        <h1>Admin Page</h1>
        <h3>Suspend User</h3>
        <Form noValidate validated={validated} onSubmit={handleSubmit}>
          <Col className="mb-3">
            <Form.Group as={Col} md="4" controlId="form1">
              <Form.Label>User ID</Form.Label>
              <Form.Control
                type="text"
                placeholder="User ID"
                required
                style={{ width: "300px" }}
                onChange={handleUserIdChange}
              />
            </Form.Group>
          </Col>
          <Button type="submit">Suspend User</Button>
        </Form>
        <h3>Support Emails:</h3>
        {emailsLoading && <div>Loading support emails...</div>}
        <Table striped bordered>
          <tbody>
            <tr>
              <th>Sender</th>
              <th>Body</th>
            </tr>
            {emails.map((email) => (
              <tr key={email.id}>
                <td>{email.sender}</td>
                <td>{email.body}</td>
              </tr>
            ))}
          </tbody>
        </Table>
        <h3>Flagged Items:</h3>
        {flaggedItemsLoading && <div>Loading flagged items...</div>}
        <Table striped bordered>
          <tbody>
            <tr>
              <th>Name</th>
              <th>Description</th>
            </tr>
            {flaggedItems.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.descrition}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    );
  } else {
    return (
      <div>
        <Link to="/dashboard">Back to dashboard</Link>
        <div>You are not the admin! Come back when your username is "admin"!</div>
      </div>
    );
  }
};

export default AdminPage;
