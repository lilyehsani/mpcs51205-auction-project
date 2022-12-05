import React, { useEffect } from "react";
import axios from "axios";
import { useState } from "react";
import { API_ROUTES, APP_ROUTES } from "../utils/constants";
import { Link, useNavigate } from "react-router-dom";
import { useUser } from "../lib/customHooks";
import { storeTokenInLocalStorage, getAuthenticatedUser, destroyToken } from "../lib/common";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const SignOut = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [validated, setValidated] = useState(false);
  const [user, setUser] = useState({});

  useEffect(() => {
    getAuthenticatedUser().then((value) => setUser(value));
  }, []);

  const handleClick = (event) => {
    destroyToken();
  };

  const handleDeleteAccount = async () => {
        axios
          .delete("http://127.0.0.1:5005/account/" + user.id)
          .then((resp) => console.log(resp.status));
  };

  return (
    <div style={{ display: "flex", justifyContent: "space-evenly", marginTop: "100px" }}>
        <Button
            variant="primary"
            onClick={handleClick}
        >
        Sign Out
        </Button>
        <Button
            variant="primary"
            onClick={handleDeleteAccount}
        >
        Delete Account
        </Button>
    </div>
  );
};

export default SignOut;