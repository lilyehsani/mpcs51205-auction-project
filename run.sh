pwd

docker stop InventoryDB || true
docker rm InventoryDB || true
docker rmi randomteam:inventory || true
docker run -d --hostname inventorydb --name InventoryDB mongo

docker image build -t randomteam:inventory ./inventory
docker stop Inventory || true
docker rm Inventory || true
docker run -p 5001:5000 -d --hostname inventory --name Inventory --link InventoryDB:inventorydb randomteam:inventory

