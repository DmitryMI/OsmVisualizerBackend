#!/usr/bin/bash

docker build --tag carto-image ./ 
if [ $? != 0 ]; then exit 1; fi

if [ ! -z $(docker ps -a -q -f name=carto-container) ]
then
    docker remove carto-container
fi


echo "Running Carto..."
osm_data=$(realpath ../osm-data)
carto=$(realpath ../openstreetmap-carto)
docker run -it --name carto-container --network=host --volume $carto:/openstreetmap-carto --volume $osm_data:/osm-data carto-image /container-init/generate-mapnik-style.sh

echo "Stopping Carto"
# docker stop carto-container
