import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import ItemPage from "./components/ItemPage";
import { APP_ROUTES } from "./utils/constants";
import "bootstrap/dist/css/bootstrap.min.css";
// import CreateItem from "./components/CreateItem";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<Navigate to={APP_ROUTES.DASHBOARD} />} />
        <Route path={APP_ROUTES.SIGN_UP} exact element={<SignUp />} />
        <Route path={APP_ROUTES.SIGN_IN} element={<SignIn />} />
        <Route path={APP_ROUTES.DASHBOARD} element={<Dashboard />} />
        {/* <Route path={APP_ROUTES.CREATE_ITEM} element={<CreateItem />} /> */}
        <Route path={APP_ROUTES.ITEM_PAGE} element={<ItemPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
