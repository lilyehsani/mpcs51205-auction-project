import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import { API_ROUTES, APP_ROUTES } from '../utils/constants';
import { Link, useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import InputGroup from 'react-bootstrap/InputGroup';
import Row from 'react-bootstrap/Row';

const SignUp = () => {
  const navigate = useNavigate()
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [validated, setValidated] = useState(false);

const handleSubmit = (event) => {
  const form = event.currentTarget;
  if (form.checkValidity() === false) {
    event.preventDefault();
    event.stopPropagation();
  }
  console.log(email);
  setValidated(true);
};

  const signUp = async () => {
    try {
      setIsLoading(true);
      const response = await axios({
        method: 'POST',
        url: API_ROUTES.SIGN_UP,
        data: {
          email,
          password
        }
      });
      if (!response?.data?.token) {
        console.log('Something went wrong during signing up: ', response);
        return;
      }
      navigate(APP_ROUTES.SIGN_IN);
    }
    catch (err) {
      console.log('Some error occured during signing up: ', err);
    }
    finally {
      setIsLoading(false);
    }
  };

  const handleNameChange = (value) => {
    setName(value.target.value);
  }

  const handleUsernameChange = (value) => {
    setUsername(value.target.value);
  }

  const handlePasswordChange = (value) => {
    setPassword(value.target.value);
  }

  const handleEmailChange = (value) => {
    setEmail(value.target.value);
  }

  return (
    <Form noValidate validated={validated} onSubmit={handleSubmit}>
      <Col className="mb-3">
        <Form.Group as={Col} md="4" controlId="validationCustom01">
          <Form.Label>Name</Form.Label>
          <Form.Control
            required
            type="text"
            placeholder="Name"
            required
            onChange={handleNameChange}
          />
        </Form.Group>
        <Form.Group as={Col} md="4" controlId="validationCustom02">
          <Form.Label>Username</Form.Label>
          <Form.Control
            required
            type="text"
            placeholder="Username"
            required
            onChange={handleUsernameChange}
          />
        </Form.Group>
        <Form.Group as={Col} md="4" controlId="validationCustom03">
          <Form.Label>Password</Form.Label>
          <Form.Control
            required
            type="text"
            placeholder="Password"
            required
            onChange={handlePasswordChange}
          />
        </Form.Group>
        <Form.Group as={Col} md="4" controlId="validationCustom04">
          <Form.Label>Email</Form.Label>
          <Form.Control
            required
            type="text"
            placeholder="Email"
            required
            nChange={handleEmailChange}
          />
        </Form.Group>
      </Col>
      <Button type="submit">Submit form</Button>
    </Form>
  );
}

export default SignUp;
