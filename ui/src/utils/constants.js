const API_URL = "http://localhost:3000";
export const API_ROUTES = {
  SIGN_UP: `${API_URL}/auth/signup`,
  SIGN_IN: `${API_URL}/auth/signin`,
  GET_USER: `${API_URL}/auth/me`,
};

export const APP_ROUTES = {
  SIGN_UP: "/signup",
  SIGN_IN: "/signin",
  SIGN_OUT: "/signout",
  ADMIN_PAGE: "/admin_page",
  DASHBOARD: "/dashboard",
  CREATE_AUCTION: "create_auction",
  CREATE_ITEM: "/createitem",
  ITEM_LIST: "/item_list",
  ITEM_PAGE: "/item/:itemId",
  WATCH_LIST: "/watchlist",
  SALE_ITEMS: "/saleitems",
  CART_PAGE: "/cart",
};
