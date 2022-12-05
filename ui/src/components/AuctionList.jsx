import AuctionAdminRow from "./AuctionAdminRow";
import { useState } from "react";
import axios from "axios";

const AuctionList = () => {
    const [auctions, setAuctions] = useState([]);

    const getCurrentAuctions = async (sort_end_desc) => {
        let url = "http://localhost:5003/get_all_auction";
        if (sort_end_desc === true) {
            url += "?sort_end_time=True"
        }
        axios.get(url)
            .then((response) => {
                console.log(response);
                if (response?.status != 200) {
                    console.log("get_all_auction error");
                    return;
                }
                console.log(response.data);
                if (!response.data.status) {
                    console.log(response.data);
                    return;
                }
                let resp_auction = response.data.data;
                if (resp_auction.length == 0) {
                    alert("no current auctions found");
                    return;
                }
                setAuctions(resp_auction);
            }, (error) => {
                console.log(error);
            });
    }

    return (
        <div>
            <div>Auction List</div>
            <div>
                {/* <tr>
                    <th>Auction ID</th>
                    <th>Start time</th>
                    <th>End time</th>
                    <th>Status</th>
                    <th>Starting price</th>
                    <th>Current highest bid amount</th>
                    <th>Current highest bid id</th>
                    <th>Current highest bidder</th>
                </tr> */}
                {auctions.map((auction) => (
                    <AuctionAdminRow key={auction.id} auction={auction} />
                ))}
            </div>
            <button onClick={() => { getCurrentAuctions(); }}>Refresh and get auctions</button>
            <button onClick={() => { getCurrentAuctions(true); }}>Refresh and get auctions(ending soonest displayed first)</button>
        </div>

    );
}

export default AuctionList;