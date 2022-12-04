import { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const SaleItems = () => {
    const testUID = "test101";
    const [items, setItems] = useState([]);

    const removeItemForSale = async (itemID) => {
        axios.post("http://127.0.0.1:5002/remove_item_for_sale", {
            user_id: testUID,
            item_id: parseInt(itemID),
        }, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'accept': "application/json",
            }
        })
            .then((response) => {
                console.log(response);
                if (response?.status != 200) {
                    console.log("remove_item_for_sale error");
                    return;
                }
                if (!response?.data?.status) {
                    alert(response?.data?.err_msg);
                    return;
                }
                alert("click the refresh button to see the result");
                return;
            }, (error) => {
                console.log(error);
            });        
    }

    const getSaleItems = async () => {
        axios.get("http://localhost:5002/get_items_for_sale?user_id=" + testUID)
            .then((response) => {
                console.log(response);
                if (response?.status != 200) {
                    console.log("get_items_for_sale error");
                    return;
                }
                if (!response.data.status) {
                    console.log(response.data);
                    return;
                }
                let resp_items = response.data.data;
                if (resp_items === null) {
                    setItems([]);
                    // alert("no items found");
                    return;
                }
                let array = [];
                for (let i = 0; i < resp_items.length; i++) {
                    let cur_url = "/item/" + resp_items[i].id;
                    array.push(
                        <div key={resp_items[i].id}>
                            <div>{resp_items[i].id} - {resp_items[i].name} - {resp_items[i].description}</div>
                            <Link to={cur_url}>see details</Link>
                            <button onClick={() => {removeItemForSale(resp_items[i].id);}}>Delete it</button>
                        </div>

                    );
                }
                setItems(array);
            }, (error) => {
                console.log(error);
            });
    };

    return (
        <div>
            <div>Your items currently selling</div>
            <div className="p-5 bg-light border">
            <button onClick={() => { (getSaleItems()) }}>Refresh</button>
            <div>Click to refresh and see your items on sale. (Empty if no items are on sale)</div>
                <div className="p-3 bg-light border">
                {items}
                </div>  
            </div>
            <div>
                <Link to="/createitem">Create an item</Link>
            </div>
            <div>
                <Link to="/dashboard">Back to dashboard</Link>
            </div>
        </div>

    );
}

export default SaleItems;