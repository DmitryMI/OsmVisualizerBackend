#!/bin/bash

# Rebuilding not needed! Script is inside a volume.

set -e

cd /openstreetmap-carto

./scripts/get-external-data.py -U postgres --password postgres --host localhost --port 5432

if [ ! -d ./fonts ]
then
    mkdir -p ./fonts
    ./scripts/get-fonts.sh
else
    echo "fonts seem to be already downloaded. Delete $(pwd)/fonts to reload the fonts."
fi

cd /osm-data

for FILE in *;
do 
    echo $FILE;
    osm2pgsql -d gis -U postgres --create --slim -G --hstore --tag-transform-script /openstreetmap-carto/openstreetmap-carto.lua -C 3000 --number-processes 8 -S /openstreetmap-carto/openstreetmap-carto.style $FILE
done

cd /openstreetmap-carto
export PGPASSWORD='postgres'; psql -h localhost -p 5432 -d gis -f indexes.sql -U postgres 

