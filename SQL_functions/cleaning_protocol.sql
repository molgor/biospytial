-- Cleaning script version 1.0.
-- In order to clean the gbif databases and have a more "normalized" form of it.
-- The records without any information of species, genus,family,class,order,phylum and kingdom are deleted.
-- Also records with no id key (working as foreign keys for species, genus, family, class, order, phylum and kingdom are deleted.
-- @author: Juan Escamilla
-- 24/10/2014

\echo 'Borrando registros de species_id nulos';
DELETE  FROM gbif_occurrence where species_id isNull;

\echo 'Creando tabla de registros sin genero';
CREATE TABLE no_genusname_occurrence AS (SELECT *  FROM gbif_occurrence WHERE  ((genus isNULL or genus = 'incertae sedis') OR (genus_id isNull)) );
\echo 'Borrando genus vacio';
DELETE FROM gbif_occurrence where genus isNULL or genus = 'incertae sedis' OR genus_id isNull;

\echo 'Creando tabla de registros sin familia';
CREATE TABLE no_familyname_occurrence AS (SELECT *  FROM gbif_occurrence WHERE  ((family isNULL or family = 'incertae sedis') OR (family_id isNull)));
\echo 'Borrando family vacio';
DELETE FROM gbif_occurrence where family isNULL or family = 'incertae sedis' OR family_id isNull;

\echo 'Creando tabla de registros sin clase';
CREATE TABLE no_classname_occurrence AS (SELECT *  FROM gbif_occurrence WHERE  (( _class isNULL or _class = 'incertae sedis') OR (class_id isNull) ));
\echo 'Borrando _class vacio';
DELETE FROM gbif_occurrence where _class isNULL or _class = 'incertae sedis' OR class_id isNull;

\echo 'Creando tabla de registros sin orden';
CREATE TABLE no_ordername_occurrence AS (SELECT *  FROM gbif_occurrence WHERE  (( _order isNULL or _order = 'incertae sedis') OR (order_id isNull) ));
\echo 'Borrando _order vacio';
DELETE FROM gbif_occurrence where _order isNULL or _order = 'incertae sedis' OR order_id isNull;

\echo 'Creando tabla de registros sin phylum';
CREATE TABLE no_phylumname_occurrence AS (SELECT *  FROM gbif_occurrence WHERE  (( phylum isNULL or phylum = 'incertae sedis') OR (phylum_id isNull) ) );
\echo 'Borrando phylum vacio';
DELETE FROM gbif_occurrence where phylum isNULL or phylum = 'incertae sedis' OR phylum_id isNull;

\echo 'Creando tabla de registros sin kingdom';
CREATE TABLE no_kingdomname_occurrence AS (SELECT *  FROM gbif_occurrence WHERE  (( kingdom isNULL or kingdom = 'incertae sedis') OR (kingdom_id isNull) ));
\echo 'Borrando kingdom vacio';DELETE FROM gbif_occurrence where kingdom isNULL or kingdom = 'incertae sedis' OR kingdom_id isNull;


\echo 'Limpiando and reindexing table';
VACUUM ANALYZE gbif_occurrence;