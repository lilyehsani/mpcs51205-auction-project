import React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import "./index.css";
import moment from "moment";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import { getAuthenticatedUser } from "../lib/common";
import AdminPage from "./AdminPage";

const AdminEmailRow = (props) => {
  const [response, setResponse] = useState("");

  const sendResponse = async () => {
    try {
      console.log(response, props.email.sender);
      const resp = await axios.post(
        "http://127.0.0.1:5007/send_email",
        {
          subject: "Response to your inquiry.",
          body: response,
          to: props.email.sender,
        },
        {
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            accept: "application/json",
          },
        }
      );
      if (resp.data.status) {
        try {
          const resp = await axios.patch(
            "http://127.0.0.1:5006/register_response?id=" + props.email.id
          );
          if (resp.data.status) {
            alert("Email was sent and response was recorded.");
            window.location.reload(false);
          } else {
            alert("Email was sent but response could not be recorded. Reason: " + resp.data.er_msg);
          }
        } catch (error) {
          console.error(error);
        }
      } else {
        alert("Email could not be sent.");
      }
    } catch (error) {
      console.log(error);
    }
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    e.stopPropagation();
    console.log(response);
    sendResponse();
  };

  const handleResponseChange = (value) => {
    setResponse(value.target.value);
  };

  return (
    <tr key={props.email.id}>
      <td>{props.email.sender}</td>
      <td>{props.email.body}</td>
      <td>{props.email.responded_time === null ? "No" : "Yes"}</td>
      <td>
        <Form noValidate onSubmit={handleSubmit}>
          <Col className="mb-3">
            <Form.Group as={Col} md="4">
              <Form.Label>Response:</Form.Label>
              <Form.Control
                required
                type="text"
                placeholder="Respond here"
                onChange={handleResponseChange}
              />
            </Form.Group>
          </Col>
          <Button type="submit">Send response</Button>
        </Form>
        <div>
          This operation can take time and will alert you when it is complete. Please only press the
          button once.
        </div>
      </td>
    </tr>
  );
};

export default AdminEmailRow;
