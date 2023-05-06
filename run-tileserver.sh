#!/bin/bash

if [ ! -z $(docker ps -a -q -f name=mapnik-container) ]
then
    docker remove mapnik-container
fi

docker start postgis-container

scripts=$(realpath ./mapnik/scripts)
tilecache=$(realpath ./mapnik/tilecache)
carto=$(realpath ./openstreetmap-carto)
mkdir -p tilecache

# docker run -it --name mapnik-container --network=host --volume $scripts:/scripts --volume $tilecache:/tilecache mapnik-image /scripts/run-tileserver.sh

docker run -it --name mapnik-container -p 7654:7654 -p 8081:8081 --volume $scripts:/scripts --volume $carto:/openstreetmap-carto --volume $tilecache:/tilecache mapnik-image /scripts/run-tileserver.sh
