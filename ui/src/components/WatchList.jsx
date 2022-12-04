import { useState } from 'react';
import axios from 'axios';


const WatchList = () => {
    const [maxPrice, setMaxPrice] = useState(0);
    const [categoryID, setCategoryID] = useState(0);
    const [watchList, setWatchList] = useState([]);
    const [categories, setCategories] = useState([]);
    const [categoryIDList, setCategoryIDList ] = useState([]);

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
                let category_id_array = []
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
        axios.post("http://localhost:5002/create_watch_list", {
            user_id:"test101",
            category_id: categoryID,
            max_price: maxPrice
        }, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type':  'application/json',
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
            <div>welcome WatchList</div>
            <div>
                <div className="p-5 bg-light border">Add a watch list</div>

                <div className="p-3 bg-light border">
                    <button
                        onClick={() => { (getAllCategories()) }}>
                        Get all the categories
                    </button>
                    <div>
                        {categories}
                    </div>
                </div>
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
                <button onClick={() => {addWatchList();}}>Add watch list</button>
            </div>
        </div>



    );
}

export default WatchList;