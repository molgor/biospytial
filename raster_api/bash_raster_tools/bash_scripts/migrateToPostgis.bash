#!/bin/bash

# This script generates a sql file with a single table compound of 12 bands (one for each month)

# Input bioclim 

FILENAME=$1



echo  "Processing: "${FILENAME}.vrt

TABLE=$(basename -s .tif $FILENAME)


gdalbuildvrt -separate $TABLE.vrt $FILENAME


echo "Generating SQL table"
raster2pgsql -d -I -C -M -F -t 128x128 $TABLE.vrt ${TABLE} > ${TABLE}.sql

echo "Ingesting in DB"
psql -d biospytial -h panthera -U biospytial -f ${TABLE}.sql

echo "Removing table"
#rm ${TABLE}.sql

echo $TABLE

