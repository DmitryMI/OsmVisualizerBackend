#!/bin/bash

osm_data=$(realpath ./postgis/osm-data)
wd=$(pwd)
if [ ! -d $osm_data ]
then
    mkdir -p $osm_data
    cd $osm_data
    wget https://download.geofabrik.de/asia/azerbaijan-latest.osm.pbf
    cd $wd
fi

cd ./postgis
./build.sh
if [ $? != 0 ]; then exit 1; fi
cd ..

if [ ! -d ./openstreetmap-carto ] 
then
    git clone https://github.com/gravitystorm/openstreetmap-carto
fi

carto=$(realpath ./openstreetmap-carto)
postgis_scripts=$(realpath ./postgis/scripts)
echo "Starting PostGis in detached mode on port 5432..."

if [ -z $(docker ps -a -q -f name=postgis-container) ]
then
    docker run -e POSTGRES_PASSWORD=postgres --name postgis-container -d -p 5432:5432 --volume $carto:/openstreetmap-carto --volume $osm_data:/osm-data --volume $postgis_scripts:/scripts postgis-image
    if [ $? != 0 ]; then exit 1; fi
else
    echo "Container postgis-container already exists. Starting..."
    docker start postgis-container
fi

echo "Waiting for PostGis to startup..."
sleep 3

cd ./carto
./build.sh
if [ $? != 0 ]; then exit 1; fi
cd ..

cd ./mapnik
./build.sh
if [ $? != 0 ]; then exit 1; fi

#echo "Stopping PostGis"
#docker stop postgis-container

