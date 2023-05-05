FROM postgres

RUN apt-get -y update

RUN apt-get install -y postgis
RUN apt install -y osm2pgsql
RUN apt install -y python3 python-is-python3

# Unix user for PostGIS
RUN useradd -m renderaccount
RUN printf "renderaccount\nrenderaccount" | passwd "renderaccount"

RUN apt-get install -y libyaml-dev
RUN apt-get install -y python3-pip
RUN pip install pyYaml
RUN python -m pip install requests
RUN pip install psycopg2-binary
RUN apt-get install -y gdal-bin
RUN apt-get install -y curl
RUN apt-get install -y zip unzip

COPY ./docker-entrypoint-initdb.d /docker-entrypoint-initdb.d

