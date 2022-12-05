import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";


const Category = () => {
    const [categories, setCategories] = useState([]);
    const [name, setName] = useState("");
    const [categoryID, setCategoryID] = useState(0);


    const getAllCategories = async () => {
        axios.get("http://localhost:5001/get_all_categories").then(
            (response) => {
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
                        <div key={resp_categories[i].id}>
                            ID: {resp_categories[i].id} - Name: {resp_categories[i].name}
                        </div>
                    );
                }
                setCategories(categories_array);
            },
            (error) => {
                console.log(error);
            }
        );
    };

    const addCategory = async () => {
        if (name == "") {
            alert("fill a name before creating");
            return;
        }
        axios.post("http://127.0.0.1:5001/create_category", {
            name: name
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
                    console.log("create_category error");
                    return;
                }
                if (response?.data.status == false) {
                    alert(response?.data.err_msg);
                    return;
                }
                alert("created successfully");
            }, (error) => {
                console.log(error);
            });
    }

    const deleteCategory = async () => {
        if (categoryID == 0) {
            alert("fill a categoryid before deleting");
            return;
        }
        axios.post("http://127.0.0.1:5001/delete_category", {
            id: categoryID
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
                    console.log("delete_category error");
                    return;
                }
                if (response?.data.status == false) {
                    alert(response?.data.err_msg);
                    return;
                }
                alert("deleted successfully");
            }, (error) => {
                console.log(error);
            });
    }

    return (
        <div className="p-5 bg-light border">
            <Link to="/dashboard">Back to dashboard</Link>
            <h1>Category page</h1>
            <p>Note: Click the get all button to see the result after creating or deleting</p>
            <div className="p-3 bg-light border">
                <h3>Part1: Get all categories</h3>
                <button
                    onClick={() => {
                        getAllCategories();
                    }}>
                    Get all the categories
                </button>
                <div>{categories}</div>
            </div>

            <div className="p-3 bg-light border">
                <h3>Part2: Add a category</h3>
                <input type="text"
                    placeholder="new category name"
                    value={name}
                    onChange={(e) => { setName(e.target.value); }}></input>
                <button
                    onClick={() => {
                        addCategory();
                    }}>
                    Add
                </button>
            </div>

            <div className="p-3 bg-light border">
                <h3>Part3: Delete a category</h3>
                <p>Enter a valid category id. You can find them in the part 1</p>
                <input type="number"
                    placeholder="category id"
                    value={categoryID}
                    onChange={(e) => { setCategoryID(e.target.value); }}></input>
                <button
                    onClick={() => {
                        deleteCategory();
                    }}>
                    Delete
                </button>
            </div>
        </div>
    )
}

export default Category;