FROM ubuntu:22.04

RUN apt-get -y update

RUN apt install -y python3 python-is-python3 git make wget

# Mapnik source code
RUN mkdir ~/software
WORKDIR ~/software
RUN git clone https://github.com/mapnik/mapnik.git --depth 10
WORKDIR ./mapnik
RUN git submodule update --init

# Fix bug in Mapnik's source code
COPY ./mapnik/test/unit/text/script_runs.cpp ./test/unit/text/script_runs.cpp

# Scons (for building Mapnik)
RUN apt-get install -y gcc python3-pip scons

# Clang
RUN apt-get install -y software-properties-common
ENV CLANG_VERSION=15
RUN wget https://apt.llvm.org/llvm.sh
RUN chmod +x llvm.sh
RUN ./llvm.sh $CLANG_VERSION

RUN apt install -y curl
RUN ./bootstrap.sh
RUN ./configure CXX="clang++-$CLANG_VERSION" CC="clang-$CLANG_VERSION" USE_BOOST_FILESYSTEM=true
# RUN ./configure CXX="g++" CC="gcc" CXX_STD="20"
RUN JOBS=32 make
RUN make install

# Fonts
RUN apt-get install -y fonts-noto-cjk fonts-noto-hinted fonts-noto-unhinted

# Web server
RUN apt install -y apache2
RUN apt install -y libapache2-mod-tile renderd

# RUN echo "LoadModule tile_module /usr/lib/apache2/modules/mod_tile.so" > /etc/apache2/mods-available/mod_tile.load

# RUN ln -s /etc/apache2/mods-available/mod_tile.load /etc/apache2/mods-enabled/

COPY ./mod_tile/etc/renderd/renderd.conf /etc/renderd.conf
COPY ./mod_tile/etc/apache2/renderd-example-map.conf /etc/apache2/conf-available/renderd-example-map.conf

COPY ./mod_tile/utils/example-map /var/www/example-map
