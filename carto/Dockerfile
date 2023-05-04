FROM ubuntu:22.04

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update

RUN apt install -y python3 python-is-python3

# Custom indexes
RUN apt-get install -y postgresql-client

# For data import
RUN apt install -y osm2pgsql

# CartoCSS
RUN apt install -y npm
RUN npm install -g carto
RUN apt install -y python3-pip
RUN pip install pyyaml
RUN apt install curl
RUN apt install -y gdal-bin

COPY ./container-init /container-init

