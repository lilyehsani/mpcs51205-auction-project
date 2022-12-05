import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import CreateAuction from "./components/CreateAuction";
import CreateItem from "./components/CreateItem";
import ItemList from "./components/ItemList";
import ItemPage from "./components/ItemPage";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import SignOut from "./components/SignOut";
import WatchList from "./components/WatchList";
import { APP_ROUTES } from "./utils/constants";
import "bootstrap/dist/css/bootstrap.min.css";
import SaleItems from "./components/SaleItems";
import Cart from "./components/Cart";
import AdminPage from "./components/AdminPage";
import AuctionList from "./components/AuctionList";
import Category from "./components/Category";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<Navigate to={APP_ROUTES.DASHBOARD} />} />
        <Route path={APP_ROUTES.SIGN_UP} exact element={<SignUp />} />
        <Route path={APP_ROUTES.SIGN_IN} element={<SignIn />} />
        <Route path={APP_ROUTES.ADMIN_PAGE} element={<AdminPage />} />
        <Route path={APP_ROUTES.SIGN_OUT} element={<SignOut />} />
        <Route path={APP_ROUTES.DASHBOARD} element={<Dashboard />} />
        <Route path={APP_ROUTES.CREATE_AUCTION} element={<CreateAuction />} />
        <Route path={APP_ROUTES.CREATE_ITEM} element={<CreateItem />} />
        <Route path={APP_ROUTES.ITEM_LIST} element={<ItemList />} />
        <Route path={APP_ROUTES.ITEM_PAGE} element={<ItemPage />} />
        <Route path={APP_ROUTES.WATCH_LIST} element={<WatchList />} />
        <Route path={APP_ROUTES.SALE_ITEMS} element={<SaleItems />} />
        <Route path={APP_ROUTES.CART_PAGE} element={<Cart />} />
        <Route path={APP_ROUTES.AUCTION_LIST} element={<AuctionList />} />
        <Route path={APP_ROUTES.CATEGORY} element={<Category />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
