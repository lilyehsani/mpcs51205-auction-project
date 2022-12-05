import Table from 'react-bootstrap/Table';
const Dashboard = () => {
  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>#</th>
          <th>Operation</th>
          <th>Link</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td>Dashboard Page</td>
          <td><a href="http://localhost:3000/dashboard"> Dashboard page link </a> </td>
        </tr>
        <tr>
          <td>2</td>
          <td>Sign Up Page</td>
          <td><a href="http://localhost:3000/signup"> Sign up link </a> </td>
        </tr>
        <tr>
          <td>3</td>
          <td>Sign In Page</td>
          <td><a href="http://localhost:3000/signin"> Sign in link </a> </td>
        </tr>
        <tr>
          <td>4</td>
          <td>Sign Out Page</td>
          <td><a href="http://localhost:3000/signout"> Sign out link </a> </td>
        </tr>
        <tr>
          <td>5</td>
          <td>Admin Page</td>
          <td><a href="http://localhost:3000/admin_page"> Admin page link </a> </td>
        </tr>
        <tr>
          <td>6</td>
          <td>Item List Page</td>
          <td><a href="http://localhost:3000/item_list"> Item page link </a> </td>
        </tr>
        <tr>
          <td>7</td>
          <td>Create Item Page</td>
          <td><a href="http://localhost:3000/createitem"> Create item page link </a> </td>
        </tr>
        <tr>
          <td>8</td>
          <td>Item Page</td>
          <td><a href="http://localhost:3000/item/:itemId"> Item page link </a> </td>
        </tr>
        <tr>
          <td>9</td>
          <td>Create Auction Page</td>
          <td><a href="http://localhost:3000/create_auction"> Create auction page link </a> </td>
        </tr>
        <tr>
          <td>10</td>
          <td>Watchlist Page</td>
          <td><a href="http://localhost:3000/watchlist"> Watchlist page link </a> </td>
        </tr>
        <tr>
          <td>11</td>
          <td>Sell Item Page</td>
          <td><a href="http://localhost:3000/saleitems"> Sell Items page link </a> </td>
        </tr>
        <tr>
          <td>11</td>
          <td>Cart Item Page</td>
          <td><a href="http://localhost:3000/cart"> Cart page link </a> </td>
        </tr>
        <tr>
          <td>12</td>
          <td>Category Page</td>
          <td><a href="http://localhost:3000/category"> Category page link </a> </td>
        </tr>
      </tbody>
    </Table>
  );
}

export default Dashboard;