import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import CreateAuction from "./components/CreateAuction";
import CreateItem from "./components/CreateItem";
import ItemList from "./components/ItemList";
import ItemPage from "./components/ItemPage";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import WatchList from "./components/WatchList";
import { APP_ROUTES } from "./utils/constants";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<Navigate to={APP_ROUTES.DASHBOARD} />} />
        <Route path={APP_ROUTES.SIGN_UP} exact element={<SignUp />} />
        <Route path={APP_ROUTES.SIGN_IN} element={<SignIn />} />
        <Route path={APP_ROUTES.DASHBOARD} element={<Dashboard />} />
        <Route path={APP_ROUTES.CREATE_AUCTION} element={<CreateAuction />} />
        <Route path={APP_ROUTES.CREATE_ITEM} element={<CreateItem />} />
        <Route path={APP_ROUTES.ITEM_LIST} element={<ItemList />} />
        <Route path={APP_ROUTES.ITEM_PAGE} element={<ItemPage />} />
        <Route path={APP_ROUTES.WATCH_LIST} element={<WatchList />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
