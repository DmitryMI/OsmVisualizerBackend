#!/bin/bash

rm /etc/apache2/conf-available/renderd.conf

a2enmod tile
# a2enconf renderd
a2enconf renderd-example-map

service apache2 start

mkdir /var/run/renderd

renderd -f
