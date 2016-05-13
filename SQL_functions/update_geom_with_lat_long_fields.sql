--ONly intented to use the data from the columns longitude, latitude and insert into column geo.

UPDATE gbif_occurrence_csv SET geom = ST_GeomFromText(S.C,4326)
FROM
(SELECT 'POINT('|| longitude::text || ' ' || latitude::text || ')' as C from gbif_occurrence_csv) AS S



