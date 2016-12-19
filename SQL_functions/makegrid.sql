-- Function: mesh.makegrid(geometry, integer)

-- DROP FUNCTION mesh.makegrid(geometry, integer);

 CREATE OR REPLACE FUNCTION mesh.makegrid(bound_polygon geometry, grid_divisions integer)
	-- This functions create a partition inside a square poolygon. This function has been made for my thesis project and it doesn't have any
	-- exception handling. The result with other type of polygon is unexpected. 
	-- For example if you give a geometry (regular rectangle) with grid division 2 the function will throw a partition of the grid with four quadrants.
	-- YOu can use grid division in the fashion 2**n to generate nested grid.
	-- Author: Juan Escamilla molgor@gmail.com 
	--November , 16, 2014

  RETURNS geometry AS
$BODY$
DECLARE
  BoundM public.geometry; --Bound polygon transformed to metric projection (with metric_srid SRID)
  Xmin DOUBLE PRECISION;
  Xmax DOUBLE PRECISION;
  Ymax DOUBLE PRECISION;
  Ymin DOUBLE PRECISION;
  X DOUBLE PRECISION;
  Y DOUBLE PRECISION;
  sectors public.geometry[];
  xstep FLOAT;
  ystep FLOAT;
  i INTEGER;
  j INTEGER;
  k INTEGER;
  POL Character(500); 
BEGIN
  BoundM := $1;
  --ST_Transform($1, $3); --From WGS84 (SRID 4326) to metric projection, to operate with step in meters
  Xmin := ST_XMin(BoundM);
  Xmax := ST_XMax(BoundM);
  Ymax := ST_YMax(BoundM);
  Ymin := ST_YMin(BoundM); --current sector's corner coordinate
  Y := Ymin;
  X := Xmin;
  xstep := (Xmax - Xmin ) / grid_divisions;
  --RAISE NOTICE 'value of xstep(%)', xstep;
  ystep := (Ymax - Ymin ) / grid_divisions;
  k := -1;

	FOR i in 1..grid_divisions 
		LOOP
			FOR j in 1..grid_divisions
				LOOP
					sectors[k] := ST_GeomFromText('POLYGON(('||X||' '||Y||', '||(X+xstep)||' '||Y||', '||(X+xstep)||' '||(Y+ystep)||', '||X||' '||(Y+ystep)||', '||X||' '||Y||'))', 4326);
					X := X + xstep;
					k := k + 1;
					RAISE NOTICE 'value of X = %', X;
				END LOOP;
			X := xmin;	
			Y := Y + ystep;
		END LOOP;
			

  RETURN ST_Collect(sectors);
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
--  COST 100;
--ALTER FUNCTION mesh.makegrid(geometry, integer)
--  OWNER TO juan;
