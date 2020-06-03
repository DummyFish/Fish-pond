# Fish-pond

##setup procedure##

git clone git@github.com:DummyFish/Fish-pond.git

cd ./Fish-pond

docker build .

docker run -p8000:8080 yourusername/example-node-app

docker exec -it container_id bash

sudo flask run

now you can start the services and moniter the internet traffic to your container
