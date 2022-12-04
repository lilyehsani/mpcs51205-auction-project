import React from "react";
import axios from "axios";
import { useState } from "react";
import { API_ROUTES, APP_ROUTES } from "../utils/constants";
import { Link, useNavigate } from "react-router-dom";
import { useUser } from "../lib/customHooks";
import { storeTokenInLocalStorage, getAuthenticatedUser } from "../lib/common";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const SignIn = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [validated, setValidated] = useState(false);

  const handleSubmit = (event) => {
    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    }
    setValidated(true);
    login();
    event.preventDefault();
    event.stopPropagation();
  };

  const login = async () => {
    axios
      .post(
        "http://127.0.0.1:5005/account/login",
        {
          user_name: username,
          user_password: password,
        },
        {
          headers: {},
        }
      )
      .then((resp) => {
        storeTokenInLocalStorage(resp.data.access_token);
        console.log(getAuthenticatedUser());
      });
  };

  const handleUsernameChange = (value) => {
    setUsername(value.target.value);
  };

  const handlePasswordChange = (value) => {
    setPassword(value.target.value);
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: "100px" }}>
      <Form noValidate validated={validated} onSubmit={handleSubmit}>
        <Col className="mb-3">
          <Form.Group as={Col} md="4" controlId="validationCustom02">
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="text"
              placeholder="Username"
              required
              style={{ width: "300px" }}
              onChange={handleUsernameChange}
            />
          </Form.Group>
          <Form.Group as={Col} md="4" controlId="validationCustom03">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="text"
              placeholder="Password"
              required
              style={{ width: "300px" }}
              onChange={handlePasswordChange}
            />
          </Form.Group>
        </Col>
        <Button type="submit">Submit form</Button>
      </Form>
    </div>
  );
};

export default SignIn;
