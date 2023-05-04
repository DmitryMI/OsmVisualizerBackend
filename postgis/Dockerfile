FROM postgres

RUN apt-get -y update

RUN apt-get install -y postgis
RUN apt install -y osm2pgsql
RUN apt install -y python3 python-is-python3

# Unix user for PostGIS
RUN useradd -m renderaccount
RUN printf "renderaccount\nrenderaccount" | passwd "renderaccount"

COPY ./docker-entrypoint-initdb.d /docker-entrypoint-initdb.d

