pwd

docker stop InventoryDB || true
docker rm InventoryDB || true
docker stop ShoppingDB || true
docker rm ShoppingDB || true
docker stop Inventory || true
docker rm Inventory || true
docker stop Shopping || true
docker rm Shopping || true

docker rmi randomteam:inventory || true
docker rmi randomteam:shopping || true
docker run --hostname inventorydb --name=InventoryDB --env="MYSQL_ROOT_PASSWORD=root_password" -p 3309:3306 -d mysql:latest
docker run --hostname shoppingdb --name=ShoppingDB --env="MYSQL_ROOT_PASSWORD=root_password" -p 3307:3306 -d mysql:latest
docker image build -t randomteam:inventory ./inventory
docker image build -t randomteam:shopping ./shopping_service
echo "wait"
sleep 10
echo "start"
docker run -p 5001:5000 -dit --hostname inventory --name Inventory --link InventoryDB:inventorydb randomteam:inventory
docker run -p 5002:5000 -dit --hostname shopping --name Shopping --link ShoppingDB:shoppingdb --link Inventory:inventory randomteam:shopping