#!/usr/bin/bash

if [ ! -d ./mapnik ]
then
    git clone https://github.com/mapnik/mapnik.git --depth 10
    cd ./mapnik
    git submodule update --init
fi

if [ ! -d ./mod_tile ]
then
    git clone https://github.com/openstreetmap/mod_tile
fi

echo "Building mapnik..."
docker build --tag mapnik-image ./

