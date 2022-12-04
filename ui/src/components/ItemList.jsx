import { useState } from 'react';
import axios from 'axios';

const ItemList = () => {
    const [keyword, setKeyword] = useState('');
    const [categoryID, setcategoryID] = useState(0);
    const [items, setItems] = useState([]);
    const [categories, setCategories] = useState([]);

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
                for (let i = 0; i < resp_categories.length; i++) {
                    categories_array.push(
                        <div key={resp_categories[i].id}>{resp_categories[i].id} - {resp_categories[i].name}</div>
                    );
                }
                setCategories(categories_array);
            }, (error) => {
                console.log(error);
            });
    }

    const searchByKeyword = async () => {
        console.log(keyword);
        axios.get("http://localhost:5001/search_item?keyword=" + keyword)
            .then((response) => {
                console.log(response);
                if (response?.status != 200) {
                    console.log("search error");
                    return;
                }
                console.log(response.data.data);
                let resp_items = response.data.data;
                let array = [];
                for (let i = 0; i < resp_items.length; i++) {
                    array.push(
                        <div key={resp_items[i].id}>{resp_items[i].id} - {resp_items[i].name} - {resp_items[i].description}</div>
                    );
                }
                setItems(array);
            }, (error) => {
                console.log(error);
            });
    };

    const searchByCategoryID = async () => {
        console.log(categoryID);
        axios.get("http://localhost:5001/get_items_by_category?id=" + categoryID)
            .then((response) => {
                console.log(response);
                if (response?.status != 200) {
                    console.log("get_items_by_category error");
                    return;
                }
                console.log(response.data.data);
                let resp_category_items = response.data.data;
                let cate_item_array = [];
                for (let i = 0; i < resp_category_items.length; i++) {
                    cate_item_array.push(
                        <div key={resp_category_items[i].id}>{resp_category_items[i].id} - {resp_category_items[i].name} - {resp_category_items[i].description}</div>
                    );
                }
                setItems(cate_item_array);
            }, (error) => {
                console.log(error);
            });
    };

    const getItemByCurrentAuction = async () => {
        axios.get("http://localhost:5003/get_all_auction_items")
        .then((response) => {
            console.log(response);
            if (response?.status != 200) {
                console.log("get_all_auction_items error");
                return;
            }
            console.log(response.data);
            let resp_auction_items = response.data.data;
            let auction_item_array = [];
            for (let i = 0; i < resp_auction_items.length; i++) {
                auction_item_array.push(
                    <div key={resp_auction_items[i].id}>{resp_auction_items[i].id} - {resp_auction_items[i].name} - {resp_auction_items[i].description}</div>
                );
            }
            setItems(auction_item_array);
        }, (error) => {
            console.log(error);
        });       
    }


    return (
        <>
            <div className="p-5 bg-light border">
                <div >Method1: search items with key word</div>
                <input
                    type="text"
                    placeholder="Key word to search, e.g. apple"
                    value={keyword}
                    onChange={(e) => { setKeyword(e.target.value); }} />
                <button
                    onClick={() => { (searchByKeyword(keyword)) }}>
                    Search by key word
                </button>
            </div>

            <div className="p-5 bg-light border">
                <div>Method2: search items with by category
                    (enter category ID into the input for search)</div>
                <div className="p-3 bg-light border">
                <button
                    onClick={() => { (getAllCategories(keyword)) }}>
                    Get all the categories
                </button>
                <div>
                {categories}
                </div>
                </div>
                <div>
                    <input
                        type="text"
                        placeholder="categoryID to search, e.g. 1"
                        value={categoryID}
                        onChange={(e) => { setcategoryID(e.target.value); }} />
                    <button
                            onClick={() => { (searchByCategoryID(keyword)) }}>
                            Search by category ID
                        </button>
                </div>
            </div>

            <div className="p-5 bg-light border">
                <div>Method3: See items of current auctions</div>
                <button  onClick={() => { (getItemByCurrentAuction(keyword)) }}>Get it</button>
            </div>

            <div  className="p-5 bg-light border">
                <h1>Result Item List</h1>
<<<<<<< HEAD
                <h3>(Empty if no items satisfied requirements or no filter is selected)</h3>
=======
>>>>>>> 6cac4a4d780d6e00273f247bb32c5b26d2dada2d
                {items}
            </div>


        </>
    );
}

export default ItemList;