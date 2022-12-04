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
  setValidated(true);
  createAccount();
};

const ping = async () => {
  axios.get("http://127.0.0.1:5000/account/ping").then(resp => console.log(resp.data));
}

const createAccount = async () => {
  axios.post("http://127.0.0.1:5000/account/", {
    name: name,
    user_name: username,
    user_password: password,
    email: email
  }, {
    headers: {}
  }).then(resp => console.log(resp.data))
}

const getAccount = async () => {
  axios.get("http://127.0.0.1:5000/account/63898cf3a06e8a583f00899c").then(resp => console.log(resp.data));
}

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
    ping();
  }

  const handlePasswordChange = (value) => {
    setPassword(value.target.value);
  }

  const handleEmailChange = (value) => {
    setEmail(value.target.value);
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', marginTop: '100px'}}>
    <Form noValidate validated={validated} onSubmit={handleSubmit}>
      <Col className="mb-3">
        <Form.Group as={Col} md="4" controlId="validationCustom01">
          <Form.Label style={{ display: 'flex', justifyContent: 'center'}}>Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Name"
            required
            style={{ width: '300px'}}
            onChange={handleNameChange}
          />
          <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
        </Form.Group>
        <Form.Group as={Col} md="4" controlId="validationCustom02">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            placeholder="Username"
            required
            style={{ width: '300px'}}
            onChange={handleUsernameChange}
          />
        </Form.Group>
        <Form.Group as={Col} md="4" controlId="validationCustom03">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="text"
            placeholder="Password"
            required
            style={{ width: '300px'}}
            onChange={handlePasswordChange}
          />
        </Form.Group>
        <Form.Group as={Col} md="4" controlId="validationCustom04">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="text"
            placeholder="Email"
            required
            style={{ width: '300px'}}
          />
        </Form.Group>
      </Col>
      <Button type="submit">Submit form</Button>
    </Form>
    </div>
  );
}

export default SignUp;
