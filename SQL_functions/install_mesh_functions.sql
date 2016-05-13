#!/bin/bash
# This script will install the mesh types and functions in the database.
# YOu have to have a database called GBIF (or change accordingly) with postgis 2.x
# Created by:
# Juan M. Escamilla
# 25/04/2016

# First Create Schema GRID
psql -d gbif -f create_schema.sql
# Make Grid
psql -d gbif -f makegrid.sql
# Install build grid
psql -d gbif -f buildgrid.sql
# Install build grid on
psql -d gbif -f buildgridon.sql

