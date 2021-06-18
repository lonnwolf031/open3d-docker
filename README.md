# Run a container using the `alpine` image, mount the `/tmp`
# directory from your host into the `/container/directory`
# directory in your container, and run the `ls` command to
# show the contents of that directory.
docker run \
    -v /tmp:/container/directory \
    alpine \
    ls /container/directory



docker run -t -i -v <host_dir>:<container_dir>  ubuntu /bin/bash
docker run --rm <yourImageName>  -a API_KEY - f FILENAME -o ORG_ID
