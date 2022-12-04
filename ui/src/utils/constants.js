const API_URL = 'http://localhost:3000'
export const API_ROUTES = {
  SIGN_UP: `${API_URL}/auth/signup`,
  SIGN_IN: `${API_URL}/auth/signin`,
  GET_USER: `${API_URL}/auth/me`,
}

export const APP_ROUTES = {
  SIGN_UP: '/signup',
  SIGN_IN: '/signin',
  DASHBOARD: '/dashboard',
  CREATE_ITEM: '/createitem',
  ITEM_LIST: '/item_list',
}
