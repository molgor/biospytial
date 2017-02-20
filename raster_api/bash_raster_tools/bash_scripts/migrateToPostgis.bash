#!/bin/bash

# This script generates a sql file with a single table compound of 12 bands (one for each month)

# Input bioclim 

INPUTDIR=$1


echo  "Processing: "${INPUTDIR}.vrt


TABLE=$(echo ${INPUTDIR} | awk -F_ '{ print $3 }')

gdalbuildvrt -separate ${INPUTDIR}.vrt ${INPUTDIR}/*.tif


echo "Generating SQL table"
raster2pgsql -d -I -C -M -F -t 128x128 ${INPUTDIR}.vrt bioclim.${TABLE} > ${TABLE}.sql

echo "Ingesting in DB"
psql -d gbif -f ${TABLE}.sql

echo "Removing table"
rm ${TABLE}.sql

echo $TABLE

