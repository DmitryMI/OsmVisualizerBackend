set -e

cd ./postgis/osm-data
echo "Downloading into $(pwd)"
wget --continue https://download.geofabrik.de/europe-latest.osm.pbf
wget --continue https://download.geofabrik.de/north-america-latest.osm.pbf
wget --continue https://download.geofabrik.de/asia-latest.osm.pbf
wget --continue https://download.geofabrik.de/australia-oceania-latest.osm.pbf
wget --continue https://download.geofabrik.de/central-america-latest.osm.pbf
wget --continue https://download.geofabrik.de/south-america-latest.osm.pbf
wget --continue https://download.geofabrik.de/africa-latest.osm.pbf
wget --continue https://download.geofabrik.de/antarctica-latest.osm.pbf


cd ..
cd ..

# ./osm2db.sh
