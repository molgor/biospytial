#!/bin/bash
# This script will install the mesh types and functions in the database.
# YOu have to have a database called GBIF (or change accordingly) with postgis 2.x
# Created by:
# Juan M. Escamilla
# 25/04/2016

# Arguments: $1 HOST IP ADDR
# $2 : username 

# First Create Schema GRID
psql -d gbif -f create_schema.sql -h $1 -U $2
# Make Grid
psql -d gbif -f makegrid.sql -h $1 -U $2
# Install build grid
psql -d gbif -f buildgrid.sql -h $1 -U $2
# Install build grid on
psql -d gbif -f buildgridon.sql -h $1 -U $2

