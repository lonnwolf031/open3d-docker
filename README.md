Build a docker container
=========
docker build -t open3d-docker .

--> open3d-docker:latest

Run a docker container
=========
add --rm if container needs to be removed afterwards

`docker run -v /host/dirwith3dfile:/data open3d-docker -optionsargs

possibility 2
`docker run  --mount type=bind,source="$(pwd)"/data,target=/home/data -it open3d-docker
