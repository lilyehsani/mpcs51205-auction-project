local_config = {
    "db_host" : "localhost",
    "db_port" : 3307,
    "db_user" : "root",
    "db_pwd" : "root_password",
    "db_name" : "shopping_db"
}

docker_config = {
    "db_host" : "shoppingdb",
    "db_port" : 3306,
    "db_user" : "root",
    "db_pwd" : "root_password",
    "db_name" : "shopping_db"    
}

err_msg = {
    "micro_communication_err": "microservice communication failed",
    "parse_err": "parse microservice return data failed",
    "db_err": "db err",
    "db_not_found": "not found in db",
    "param_err": "input param invalid",
    "cannot_delete_auction_item": "cannot delete the item since there is an auction ongoing"
}