-- CREATE TABLE tests.sketches(
--   id serial NOT NULL,
--   description varchar(50)
-- );

--SELECT AddGeometryColumn('tests','sketches','geom',4326,'POLYGON',2);

--INSERT INTO tests.sketches(description,geom) VALUES ('Test metric buffer 100',ST_Buffer(ST_GeomFromText('POINT(-1.38456 50.93490)', 4326),0.2));


--UPDATE tests.sketches SET geom = (ST_Buffer(ST_GeomFromText('POINT(-1.38456 50.93490)', 4326),0.3)) WHERE id = 1;


�����������

--CREATE A FUNCTION THAT RETURNS A TABLE / PARTITION OF THE TABLE.

--CREATE OR REPLACE FUNCTION "tests".withinPoligon(polygon geometry)
--RETURNS SETOF "tests".soton
--AS
--$$
--SELECT s.* FROM tests.soton as s WHERE ST_Intersects($1,s.geom);
--$$
--LANGUAGE 'sql' VOLATILE;

--SELECT * from tests.withinpoligon( (SELECT p.geom FROM (SELECT * from tests.sketches WHERE id =2) as p) );

��
--El bueno,

--CREATE OR REPLACE FUNCTION getOccurrencesInPoligon(polygon geometry)
--RETURNS SETOF gbif_occurrence
--AS
--$$
--SELECT s.* FROM gbif_occurrence as s WHERE ST_Intersects($1,s.geom);
--$$
--LANGUAGE 'sql' VOLATILE;


--Test:
 
--SELECT * from getOccurrencesInPoligon( (SELECT p.geom FROM (SELECT * from tests.sketches WHERE id =2) as p) );

--------------------------------
-- Aggregation by species name (id) with full taxonomic order.
--DROP FUNCTION "gbif_LB/Esp"(geometry);

-- CREATE OR REPLACE FUNCTION "gbif_LB/Esp"(IN polygon geometry)
--   RETURNS TABLE( 
-- 		kingdom character varying,
-- 		 _order character varying,
-- 		  _class character varying,
-- 		   family character varying, 
-- 		   scientific_name character varying,
-- 		kingdom_id integer,
-- 		phylum_id integer,
-- 		order_id integer,
-- 		class_id integer,
-- 		family_id integer,
-- 		  species_id integer, 
-- 		   n_occurs bigint,
-- 		    geom geometry) 
-- 		    AS
-- $$
-- SELECT s.kingdom,s._order,s._class,s.family,s.scientific_name,s.kingdom_id,s.phylum_id,s.order_id,s.class_id,s.family_id,s.species_id,count(s.scientific_name),ST_ConvexHull(ST_Collect(s.geom))
-- from gbif_occurrence as s
-- WHERE ST_Intersects($1,s.geom)
-- GROUP BY s.kingdom,s._order,s._class,s.family,s.scientific_name,s.kingdom_id,s.phylum_id,s.order_id,s.class_id,s.family_id,s.species_id;
-- $$
-- LANGUAGE 'sql' VOLATILE;
-- 


-- TEST
--SELECT * from "gbif_LB/Esp"( (SELECT p.geom FROM (SELECT * from tests.sketches WHERE id =2) as p) );


-- THis function extracts the info on lat lon columns to insert it into geom

INSERT INTO test_occurrence(geom)
SELECT ST_GeomFromText(S.C,4326)
FROM
(SELECT 'POINT('|| longitude::text || ' ' || latitude::text || ')' as C from test_occurrence) AS S





UPDATE gbif_occurrence_csv SET geom = ST_GeomFromText(S.C,4326)
FROM
(SELECT 'POINT('|| longitude::text || ' ' || latitude::text || ')' as C from gbif_occurrence_csv) AS S

UPDATE gbif_occurrence_csv SET geom = ST_GeomFromText(S.C,4326)
FROM
(SELECT 'POINT('|| longitude::text || ' ' || latitude::text || ')' as C from gbif_occurrence_csv) AS S

