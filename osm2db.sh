#!/bin/bash

docker start postgis-container

docker exec postgis-container /scripts/osm2db.sh

docker stop postgis-container
