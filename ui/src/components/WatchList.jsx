import { useEffect, useState } from 'react';
import axios from 'axios';
import { getAuthenticatedUser } from "../lib/common";
import { Link } from "react-router-dom";

const WatchList = () => {
    const [maxPrice, setMaxPrice] = useState(0);
    const [categoryID, setCategoryID] = useState(0);
    const [watchList, setWatchList] = useState([]);
    const [categories, setCategories] = useState([]);
    const [categoryIDList, setCategoryIDList] = useState([]);
    const [user, setUser] = useState({});
    const testUID = "test101";

    useEffect(() => {
        getAuthenticatedUser().then((value) => setUser(value));
      }, []);

    const getAllCategories = async () => {
        axios.get("http://localhost:5001/get_all_categories")
            .then((response) => {
                console.log(response);
                if (response?.status != 200) {
                    console.log("get all categories error");
                    return;
                }
                console.log(response.data.data);
                let resp_categories = response.data.data;
                let categories_array = [];
                let category_id_array = [];
                for (let i = 0; i < resp_categories.length; i++) {
                    categories_array.push(
                        <div key={resp_categories[i].id}>{resp_categories[i].id} - {resp_categories[i].name}</div>
                    );
                    category_id_array.push(parseInt(resp_categories[i].id))
                }
                setCategoryIDList(category_id_array);
                setCategories(categories_array);
            }, (error) => {
                console.log(error);
            });
    }

    const getWatchList = async () => {
        console.log(user['id']);
        axios.get("http://localhost:5002/get_user_watch_list?user_id=" + user['id'])
            .then((response) => {
                console.log(response);
                if (response?.status != 200) {
                    console.log("get watch list error");
                    return;
                }
                console.log(response.data.data);
                let resp_watchlist = response.data.data;
                let watchlist_array = [];
                for (let i = 0; i < resp_watchlist.length; i++) {
                    console.log(resp_watchlist[i]);
                    watchlist_array.push(
                        <div key={resp_watchlist[i].id}>
                            <div>id:  {resp_watchlist[i].id} - category id:  {resp_watchlist[i].category_id} - max_price:  {resp_watchlist[i].max_price}</div>
                            <button onClick={() => { deleteWatchList(resp_watchlist[i].id); }}>Delete</button>
                        </div>
                    );
                }
                setWatchList(watchlist_array);
            }, (error) => {
                console.log(error);
            });
    }

    const deleteWatchList = async (watchListID) => {
        console.log(watchListID);
        axios.post("http://127.0.0.1:5002/delete_watch_list", {
            id: watchListID
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
                    console.log("delete_watch_list error");
                    return;
                }
            }, (error) => {
                console.log(error);
            });
    }

    const addWatchList = async () => {
        if (maxPrice <= 0) {
            alert("watch list price needs to be larger than 0");
            return;
        }
        console.log(categoryIDList);
        let categoriesSet = new Set(categoryIDList);
        console.log(categoriesSet);
        console.log(categoryID);
        if (!categoriesSet.has(parseInt(categoryID))) {
            alert("click the category list and put into valid category id");
            return;
        }
        console.log("addWatchList")
        axios.post("http://127.0.0.1:5002/add_watch_list", {
            user_id: user['id'],
            category_id: categoryID,
            max_price: maxPrice
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
                    console.log("create_watch_list error");
                    return;
                }
            }, (error) => {
                console.log(error);
            });
    }


    return (
        <div>
            <Link to="/dashboard">Back to dashboard</Link>
            <h1>welcome WatchList</h1>
            <div>Notifications will be sent through email autometically when an item satisfied the watchlist requirement is created</div>
            <div className="p-5 bg-light border">
                <h2>Part 1: Add a watch list</h2>

                <div className="p-3 bg-light border">
                    <h5>step 1: get valid categories</h5>
                    <button
                        onClick={() => { (getAllCategories()) }}>
                        Get all the categories
                    </button>
                    <h6>Note : You need to click the button to get the categories first before entering one valid for creating a watchlist</h6>
                    <div>
                        {categories}
                    </div>
                </div>
                <div className="p-3 bg-light border">
                <h5>step 2: input the max price and category id  </h5>
                    <div>
                        <p>max price</p>
                        <input type="number"
                            placeholder="max price"
                            value={maxPrice}
                            onChange={(e) => { setMaxPrice(e.target.value); }}></input>
                    </div>
                    <div>
                        <p>category</p>
                        <input type="number"
                            placeholder="category id"
                            value={categoryID}
                            onChange={(e) => { setCategoryID(e.target.value); }}></input>
                    </div>
                </div>
                <div  className="p-3 bg-light border">
                <h5>step 3: click the button to create  </h5>
                    <button onClick={() => { addWatchList(); }}>Add watch list</button>
                </div>

            </div>

            <div className="p-5 bg-light border">
                <h2>Part 2: Show your watch list</h2>
                <h5>Note: You need to click the refresh button to see the new list after creating or deleting</h5>
                <button onClick={() => { getWatchList(); }}>Refresh and show</button>
                <div>{watchList}</div>
            </div>
        </div>



    );
}

export default WatchList;