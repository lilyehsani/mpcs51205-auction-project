import axios from "axios";
const AuctionAdminRow = (props) => {
  function getAuctionStatus(status) {
    switch (status) {
      case 0:
        return "0 - Not yet started";
      case 1:
        return "1 - In progress";
      case 2:
        return "2 - Ended by time";
      case 4:
        return "4 - Canceled";
    }
  }

  const deleteAuction = async () => {
    axios
      .patch("http://127.0.0.1:5003/cancel_auction?id=" + props.auction.id, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json",
          accept: "application/json",
        },
      })
      .then(
        (response) => {
          console.log(response);
          if (response?.status != 200) {
            console.log("cancel_auction error");
            return;
          }
        },
        (error) => {
          console.log(error);
        }
      );
  };

  return (
    <div key={props.auction.id}>
      <div>Auction ID : {props.auction.id}</div>
      <div>Start time: {props.auction.start_time}</div>
      <div>End time: {props.auction.end_time}</div>
      <div>Status: {getAuctionStatus(props.auction.status)}</div>
      <div>Starting price: {props.auction.start_price}</div>
      <div>Current highest bid amount: {props.auction.current_highest_bid_amount}</div>
      <div>Current highest bid id: {props.auction.current_highest_bid_id}</div>
      <div>Current highest bidder: {props.auction.current_highest_bidder}</div>
      <button
        onClick={() => {
          deleteAuction();
        }}>
        Cancel it
      </button>
    </div>
  );
};

export default AuctionAdminRow;
