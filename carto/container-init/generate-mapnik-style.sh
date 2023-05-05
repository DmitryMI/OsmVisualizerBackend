#!/bin/bash

cd /openstreetmap-carto

if [ ! -f "./mapnik.xml" ]
then
    echo "Generating mapnik.xml..."
    carto project.mml > mapnik.xml
else
    echo "mapnik.xml already exits. Style generation skipped."
fi
