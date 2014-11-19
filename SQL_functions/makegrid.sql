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