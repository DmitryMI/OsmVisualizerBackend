#!/bin/bash

docker start postgis-container

sleep 5

docker exec postgis-container /scripts/osm2db.sh

docker stop postgis-container
