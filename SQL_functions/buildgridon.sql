-- Function: mesh.makegrid(geometry, integer)

-- DROP FUNCTION mesh.makegrid(geometry, integer);

CREATE OR REPLACE FUNCTION mesh.makegrid(bound_polygon geometry, grid_divisions integer)
  RETURNS geometry AS
$BODY$
DECLARE
  BoundM public.geometry; --Bound polygon transformed to metric projection (with metric_srid SRID)
  Xmin DOUBLE PRECISION;
  Xmax DOUBLE PRECISION;
  Ymax DOUBLE PRECISION;
  X DOUBLE PRECISION;
  Y DOUBLE PRECISION;
  sectors public.geometry[];
  xstep FLOAT;
  ystep FLOAT;
  i INTEGER;
  POL Character(500); 
BEGIN
  BoundM := $1;
  --ST_Transform($1, $3); --From WGS84 (SRID 4326) to metric projection, to operate with step in meters
  Xmin := ST_XMin(BoundM);
  Xmax := ST_XMax(BoundM);
  Ymax := ST_YMax(BoundM);
  Y := ST_YMin(BoundM); --current sector's corner coordinate
  xstep := (Xmax - Xmin ) / grid_divisions;
  RAISE NOTICE 'value of xstep(%)', xstep;
  ystep := (Ymax - Y ) / grid_divisions;
  i := -1;
  <<yloop>>
  LOOP
    IF (Y >= Ymax) THEN  --Better if generating polygons exceeds bound for one step. You always can crop the result. But if not you may get not quite correct data for outbound polygons (if you calculate frequency per a sector  e.g.)
        EXIT;
    END IF;

    X := Xmin;
    <<xloop>>
    LOOP
      IF (X >= Xmax) THEN
          EXIT;
      END IF;

      i := i + 1;
      POL := 'POLYGON(('||X||' '||Y||', '||(X+xstep)||' '||Y||', '||(X+xstep)||' '||(Y+ystep)||', '||X||' '||(Y+ystep)||', '||X||' '||Y||'))';
	RAISE NOTICE 'Polygon(%)',POL;
      sectors[i] := ST_GeomFromText('POLYGON(('||X||' '||Y||', '||(X+xstep)||' '||Y||', '||(X+xstep)||' '||(Y+ystep)||', '||X||' '||(Y+ystep)||', '||X||' '||Y||'))', 4326);

      --X := X + $2;
      RAISE NOTICE 'VAlue of X(%)', X;
      RAISE NOTICE 'value of xstep(%)', xstep;
      RAISE NOTICE 'value of Xmin(%)', Xmin;
      RAISE NOTICE 'value of Y(%)', Y;
      RAISE NOTICE 'value of Ymax(%)', Ymax;
      
     -- RAISE NOTICE 'value of grid_divisions(%)', grid_divisions;
	X := X + xstep;
	
    END LOOP xloop;
      --Y := Y + $2;
      Y := Y + ystep;
  END LOOP yloop;

  --RETURN ST_Transform(ST_Collect(sectors), ST_SRID($1));
  RETURN ST_Collect(sectors);
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION mesh.makegrid(geometry, integer)
  OWNER TO gbif;

  
 -- Function: mesh.buildmesh(geometry, integer)

-- DROP FUNCTION mesh.buildmesh(geometry, integer);

CREATE OR REPLACE FUNCTION mesh.buildmesh(polygon geometry, grid_divisions integer)
  RETURNS SETOF tests.grid AS
$BODY$
DECLARE
r record;
BEGIN
FOR r IN
  SELECT row_number() OVER(ORDER BY cell) as gid,cell FROM 
  (SELECT (
  ST_Dump(
   mesh.makegrid(polygon,grid_divisions)
   )).geom AS cell) AS q_grid
LOOP
RETURN NEXT r;
END LOOP;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION mesh.buildmesh(geometry, integer)
  OWNER TO gbif;
  
  
  
 -- Function: mesh.generategridon(geometry, character varying, integer)

-- DROP FUNCTION mesh.generategridon(geometry, character varying, integer);

CREATE OR REPLACE FUNCTION mesh.generategridon(polygon geometry, t_name character varying, grid_division integer)
  RETURNS text AS
$BODY$
DECLARE
t varchar(500);
name1 varchar(500);
idxname varchar(503);
BEGIN
name1 := 'mesh.'||t_name;
idxname := 'idx_mesh_'||t_name;
RAISE NOTICE 'name1(%)',name1;
RAISE NOTICE 'idxname(%)',idxname;
EXECUTE  format('CREATE TABLE %1$s AS (
	 SELECT * FROM mesh.buildmesh(
	 %4$L
	,%2$s));'
	|| 'ALTER TABLE %1$s ADD PRIMARY KEY ("gid");' 
	|| 'CREATE INDEX %3$s ON %1$s USING GIST ("cell");'
	,name1,grid_division,idxname,polygon) ;
--RAISE NOTICE 'Creating table: %',name1;

RETURN 'Table created';
--EXECUTE format(t);
--'CREATE TABLE IF NOT EXISTS %I AS (' || t ||','||grid_division||') )', 'mesh.' || t_name);
   END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION mesh.generategridon(geometry, character varying, integer)
  OWNER TO gbif; 