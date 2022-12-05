import React from "react";
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
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [validated, setValidated] = useState(false);

  const handleClick = (event) => {
    destroyToken();
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: "100px" }}>
        <Button
            variant="primary"
            onClick={handleClick}
        >
        Sign Out
        </Button>
    </div>
  );
};

export default SignOut;
