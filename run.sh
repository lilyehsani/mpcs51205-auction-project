pwd

docker stop InventoryDB || true
docker rm InventoryDB || true
docker stop Inventory || true
docker rm Inventory || true

docker rmi randomteam:inventory || true
docker run --hostname inventorydb --name=InventoryDB --env="MYSQL_ROOT_PASSWORD=root_password" -p 3309:3306 -d mysql:latest
docker image build -t randomteam:inventory ./inventory
docker run -p 5001:5000 -dit --hostname inventory --name Inventory --link InventoryDB:inventorydb randomteam:inventory

