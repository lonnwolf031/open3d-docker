Build a docker container
=========
`docker build -t open3d-docker .

--> open3d-docker:latest

Run a docker container
=========
add --rm if container needs to be removed afterwards


possibility 2
`docker run  --mount type=bind,source="$(pwd)"/data,target=/home/data -it open3d-docker


Make a mountable docker container
========
mkdir ~/container-data

`docker run -dit -P --name open3d-docker -v ~/container-data:/data ubuntu
` sudo docker run -it hello-demo test.py`


mount ./data to /usr/src/app
` docker run -it open3d-docker -v ./data:/usr/src/app main.py scan3d.ply