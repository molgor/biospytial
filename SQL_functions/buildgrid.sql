--DROP TYPE mesh.grid
CREATE TYPE mesh.grid AS (gid bigint, cell geometry);

--DROP FUNCTION mesh.buildmesh(geometry, integer);
CREATE OR REPLACE FUNCTION mesh.buildmesh(polygon geometry, grid_divisions integer)
	-- THis function returns a table with identification key (primary key) and geometric values based on a regular mesh.
	-- Derived from the makegrid function. 
	-- Author: Juan Escamilla M. 
	-- Nov. 17 2014
	RETURNS SETOF tests.grid AS
$BODY$
DECLARE
r record;
BEGIN
FOR r IN
  SELECT row_number() OVER(ORDER BY cell) as gid,cell FROM 
  (SELECT (
  ST_Dump(
   tests.makegrid_2d_2(polygon,4)
   )).geom AS cell) AS q_grid
LOOP
RETURN NEXT r;
END LOOP;
END;
$BODY$
  LANGUAGE plpgsql