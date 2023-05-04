#!/bin/bash

a2enmod tile
a2enconf renderd
a2enconf renderd-example-map

service apache2 start

mkdir /var/run/renderd

renderd -f
