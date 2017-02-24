BEGIN;
--
-- Create model Occurrence
--
CREATE TABLE "gbif_occurrence_csv" ("id_gbif" serial NOT NULL PRIMARY KEY, "dataset_id" text NULL, "institution_code" text NULL, "collection_code" text NULL, "catalog_number" text NULL, "basis_of_record" text NULL, "scientific_name" text NULL, "kingdom" text NULL, "phylum" text NULL, "_class" text NULL, "_order" text NULL, "family" text NULL, "genus" text NULL, "specific_epithet" text NULL, "kingdom_id" integer NULL, "phylum_id" integer NULL, "class_id" integer NULL, "order_id" integer NULL, "family_id" integer NULL, "genus_id" integer NULL, "species_id" integer NULL, "country_code" text NULL, "latitude" double precision NULL, "longitude" double precision NULL, "year" integer NULL, "month" integer NULL, "day" integer NULL, "event_date" timestamp with time zone NULL, "state_province" text NULL, "county" text NULL, "country" text NULL, "geom" geometry(POINT,4326) NOT NULL);
CREATE INDEX "gbif_occurrence_csv_geom_id" ON "gbif_occurrence_csv" USING GIST ("geom" );
--
-- Create model Occurrence_CSV
--
CREATE TABLE "gbif_occurrence_csv" ("id_gbif" serial NOT NULL PRIMARY KEY, "dataset_id" text NULL, "institution_code" text NULL, "collection_code" text NULL, "catalog_number" text NULL, "basis_of_record" text NULL, "scientific_name" text NULL, "scientific_name_author" text NULL, "taxon_id" integer NULL, "kingdom" text NULL, "phylum" text NULL, "_class" text NULL, "_order" text NULL, "family" text NULL, "genus" text NULL, "specific_epithet" text NULL, "kingdom_id" integer NULL, "phylum_id" integer NULL, "class_id" integer NULL, "order_id" integer NULL, "family_id" integer NULL, "genus_id" integer NULL, "species_id" integer NULL, "country_code" text NULL, "latitude" double precision NULL, "longitude" double precision NULL, "year" integer NULL, "month" integer NULL, "event_date" timestamp with time zone NULL, "elevation_in_meters" double precision NULL, "depth_in_meters" double precision NULL, "verbatim_scientific_name" text NULL, "taxon_rank" text NULL, "verbatim_kingdom" text NULL, "verbatim_phylum" text NULL, "verbatim_class" text NULL, "verbatim_order" text NULL, "verbatim_family" text NULL, "verbatim_genus" text NULL, "verbatim_specific_epithet" text NULL, "verbatim_infraspecific_epithet" text NULL, "verbatim_latitude" text NULL, "verbatim_longitude" text NULL, "coordinate_precision" double precision NULL, "maximum_elevation_in_meters" double precision NULL, "minimum_elevation_in_meters" double precision NULL, "elevation_precision" double precision NULL, "minimum_depth_in_meters" double precision NULL, "maximum_depth_in_meters" double precision NULL, "depth_precision" double precision NULL, "continent_ocean" text NULL, "state_province" text NULL, "county" text NULL, "country" text NULL, "recorded_by" text NULL, "locality" text NULL, "verbatim_year" text NULL, "verbatim_month" text NULL, "day" integer NULL, "verbatim_basis_of_record" text NULL, "identified_by" text NULL, "date_identified" text NULL, "created" text NULL, "modified" text NULL, "geom" geometry(POINT,4326) NULL);
CREATE INDEX "gbif_occurrence_csv_geom_id" ON "gbif_occurrence_csv" USING GIST ("geom" );
--
-- Create model Occurrence_CSV_Verbatim
--
CREATE TABLE "gbif_occurrence_csv_verbatim" ("id_gbif" serial NOT NULL PRIMARY KEY, "popo" text NULL, "dataset_id" text NULL, "institution_code" text NULL, "collection_code" text NULL, "catalog_number" text NULL, "basis_of_record" text NULL, "scientific_name" text NULL, "scientific_name_author" text NULL, "taxon_id" integer NULL, "kingdom" text NULL, "phylum" text NULL, "_class" text NULL, "_order" text NULL, "family" text NULL, "genus" text NULL, "specific_epithet" text NULL, "kingdom_id" integer NULL, "phylum_id" integer NULL, "class_id" integer NULL, "order_id" integer NULL, "family_id" integer NULL, "genus_id" integer NULL, "species_id" integer NULL, "country_code" text NULL, "latitude" double precision NULL, "longitude" double precision NULL, "year" integer NULL, "month" integer NULL, "event_date" timestamp with time zone NULL, "elevation_in_meters" text NULL, "depth_in_meters" text NULL, "verbatim_scientific_name" text NULL, "taxon_rank" text NULL, "verbatim_kingdom" text NULL, "verbatim_phylum" text NULL, "verbatim_class" text NULL, "verbatim_order" text NULL, "verbatim_family" text NULL, "verbatim_genus" text NULL, "verbatim_specific_epithet" text NULL, "verbatim_infraspecific_epithet" text NULL, "verbatim_latitude" text NULL, "verbatim_longitude" text NULL, "coordinate_precision" text NULL, "maximum_elevation_in_meters" text NULL, "minimum_elevation_in_meters" text NULL, "elevation_precision" text NULL, "minimum_depth_in_meters" text NULL, "maximum_depth_in_meters" text NULL, "depth_precision" text NULL, "continent_ocean" text NULL, "state_province" text NULL, "county" text NULL, "country" text NULL, "recorded_by" text NULL, "locality" text NULL, "verbatim_year" text NULL, "verbatim_month" text NULL, "day" integer NULL, "verbatim_basis_of_record" text NULL, "identified_by" text NULL, "date_identified" text NULL, "created" text NULL, "modified" text NULL);
CREATE INDEX "gbif_occurrence_csv_d366d308" ON "gbif_occurrence_csv" ("dataset_id");
CREATE INDEX "gbif_occurrence_csv_3720fb06" ON "gbif_occurrence_csv" ("institution_code");
CREATE INDEX "gbif_occurrence_csv_d4990130" ON "gbif_occurrence_csv" ("collection_code");
CREATE INDEX "gbif_occurrence_csv_4e8018c9" ON "gbif_occurrence_csv" ("catalog_number");
CREATE INDEX "gbif_occurrence_csv_badd05cc" ON "gbif_occurrence_csv" ("basis_of_record");
CREATE INDEX "gbif_occurrence_csv_15b0b0b7" ON "gbif_occurrence_csv" ("scientific_name");
CREATE INDEX "gbif_occurrence_csv_dc420563" ON "gbif_occurrence_csv" ("kingdom");
CREATE INDEX "gbif_occurrence_csv_dcb3a2ca" ON "gbif_occurrence_csv" ("phylum");
CREATE INDEX "gbif_occurrence_csv_71c7bd4a" ON "gbif_occurrence_csv" ("_class");
CREATE INDEX "gbif_occurrence_csv_a51fee94" ON "gbif_occurrence_csv" ("_order");
CREATE INDEX "gbif_occurrence_csv_0d3fda0b" ON "gbif_occurrence_csv" ("family");
CREATE INDEX "gbif_occurrence_csv_030e7a0c" ON "gbif_occurrence_csv" ("genus");
CREATE INDEX "gbif_occurrence_csv_e94bed27" ON "gbif_occurrence_csv" ("specific_epithet");
CREATE INDEX "gbif_occurrence_csv_afe8fbda" ON "gbif_occurrence_csv" ("kingdom_id");
CREATE INDEX "gbif_occurrence_csv_340cabd4" ON "gbif_occurrence_csv" ("phylum_id");
CREATE INDEX "gbif_occurrence_csv_301e3c17" ON "gbif_occurrence_csv" ("class_id");
CREATE INDEX "gbif_occurrence_csv_69dfcb07" ON "gbif_occurrence_csv" ("order_id");
CREATE INDEX "gbif_occurrence_csv_0caa70f7" ON "gbif_occurrence_csv" ("family_id");
CREATE INDEX "gbif_occurrence_csv_92319714" ON "gbif_occurrence_csv" ("genus_id");
CREATE INDEX "gbif_occurrence_csv_1699a6e9" ON "gbif_occurrence_csv" ("species_id");
CREATE INDEX "gbif_occurrence_csv_55eceb8d" ON "gbif_occurrence_csv" ("country_code");
CREATE INDEX "gbif_occurrence_csv_28c1e37e" ON "gbif_occurrence_csv" ("latitude");
CREATE INDEX "gbif_occurrence_csv_ba569b80" ON "gbif_occurrence_csv" ("longitude");
CREATE INDEX "gbif_occurrence_csv_84cdc76c" ON "gbif_occurrence_csv" ("year");
CREATE INDEX "gbif_occurrence_csv_7436f942" ON "gbif_occurrence_csv" ("month");
CREATE INDEX "gbif_occurrence_csv_628b7db0" ON "gbif_occurrence_csv" ("day");
CREATE INDEX "gbif_occurrence_csv_2650cd64" ON "gbif_occurrence_csv" ("event_date");
CREATE INDEX "gbif_occurrence_csv_f34e84e4" ON "gbif_occurrence_csv" ("state_province");
CREATE INDEX "gbif_occurrence_csv_aad0cd42" ON "gbif_occurrence_csv" ("county");
CREATE INDEX "gbif_occurrence_csv_e909c2d7" ON "gbif_occurrence_csv" ("country");
CREATE INDEX "gbif_occurrence_csv_dataset_id_9dde2f2b_like" ON "gbif_occurrence_csv" ("dataset_id" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_institution_code_7bffe98e_like" ON "gbif_occurrence_csv" ("institution_code" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_collection_code_100c4bfb_like" ON "gbif_occurrence_csv" ("collection_code" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_catalog_number_f730ca64_like" ON "gbif_occurrence_csv" ("catalog_number" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_basis_of_record_b6372d05_like" ON "gbif_occurrence_csv" ("basis_of_record" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_scientific_name_995ed8d1_like" ON "gbif_occurrence_csv" ("scientific_name" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_kingdom_73749a78_like" ON "gbif_occurrence_csv" ("kingdom" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_phylum_ebbea764_like" ON "gbif_occurrence_csv" ("phylum" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv__class_1f6c852d_like" ON "gbif_occurrence_csv" ("_class" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv__order_3e5b8cba_like" ON "gbif_occurrence_csv" ("_order" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_family_ee1ae770_like" ON "gbif_occurrence_csv" ("family" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_genus_054168f7_like" ON "gbif_occurrence_csv" ("genus" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_specific_epithet_80faadf0_like" ON "gbif_occurrence_csv" ("specific_epithet" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_country_code_5709f9a6_like" ON "gbif_occurrence_csv" ("country_code" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_state_province_a71e456b_like" ON "gbif_occurrence_csv" ("state_province" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_county_284ce3bf_like" ON "gbif_occurrence_csv" ("county" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_country_ec74a73b_like" ON "gbif_occurrence_csv" ("country" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_15b0b0b7" ON "gbif_occurrence_csv" ("scientific_name");
CREATE INDEX "gbif_occurrence_csv_dc420563" ON "gbif_occurrence_csv" ("kingdom");
CREATE INDEX "gbif_occurrence_csv_dcb3a2ca" ON "gbif_occurrence_csv" ("phylum");
CREATE INDEX "gbif_occurrence_csv_71c7bd4a" ON "gbif_occurrence_csv" ("_class");
CREATE INDEX "gbif_occurrence_csv_a51fee94" ON "gbif_occurrence_csv" ("_order");
CREATE INDEX "gbif_occurrence_csv_0d3fda0b" ON "gbif_occurrence_csv" ("family");
CREATE INDEX "gbif_occurrence_csv_030e7a0c" ON "gbif_occurrence_csv" ("genus");
CREATE INDEX "gbif_occurrence_csv_e94bed27" ON "gbif_occurrence_csv" ("specific_epithet");
CREATE INDEX "gbif_occurrence_csv_afe8fbda" ON "gbif_occurrence_csv" ("kingdom_id");
CREATE INDEX "gbif_occurrence_csv_340cabd4" ON "gbif_occurrence_csv" ("phylum_id");
CREATE INDEX "gbif_occurrence_csv_301e3c17" ON "gbif_occurrence_csv" ("class_id");
CREATE INDEX "gbif_occurrence_csv_69dfcb07" ON "gbif_occurrence_csv" ("order_id");
CREATE INDEX "gbif_occurrence_csv_0caa70f7" ON "gbif_occurrence_csv" ("family_id");
CREATE INDEX "gbif_occurrence_csv_92319714" ON "gbif_occurrence_csv" ("genus_id");
CREATE INDEX "gbif_occurrence_csv_1699a6e9" ON "gbif_occurrence_csv" ("species_id");
CREATE INDEX "gbif_occurrence_csv_28c1e37e" ON "gbif_occurrence_csv" ("latitude");
CREATE INDEX "gbif_occurrence_csv_ba569b80" ON "gbif_occurrence_csv" ("longitude");
CREATE INDEX "gbif_occurrence_csv_84cdc76c" ON "gbif_occurrence_csv" ("year");
CREATE INDEX "gbif_occurrence_csv_7436f942" ON "gbif_occurrence_csv" ("month");
CREATE INDEX "gbif_occurrence_csv_2650cd64" ON "gbif_occurrence_csv" ("event_date");
CREATE INDEX "gbif_occurrence_csv_scientific_name_995ed8d1_like" ON "gbif_occurrence_csv" ("scientific_name" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_kingdom_73749a78_like" ON "gbif_occurrence_csv" ("kingdom" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_phylum_ebbea764_like" ON "gbif_occurrence_csv" ("phylum" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv__class_1f6c852d_like" ON "gbif_occurrence_csv" ("_class" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv__order_3e5b8cba_like" ON "gbif_occurrence_csv" ("_order" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_family_ee1ae770_like" ON "gbif_occurrence_csv" ("family" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_genus_054168f7_like" ON "gbif_occurrence_csv" ("genus" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_specific_epithet_80faadf0_like" ON "gbif_occurrence_csv" ("specific_epithet" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_verbatim_15b0b0b7" ON "gbif_occurrence_csv_verbatim" ("scientific_name");
CREATE INDEX "gbif_occurrence_csv_verbatim_dc420563" ON "gbif_occurrence_csv_verbatim" ("kingdom");
CREATE INDEX "gbif_occurrence_csv_verbatim_dcb3a2ca" ON "gbif_occurrence_csv_verbatim" ("phylum");
CREATE INDEX "gbif_occurrence_csv_verbatim_71c7bd4a" ON "gbif_occurrence_csv_verbatim" ("_class");
CREATE INDEX "gbif_occurrence_csv_verbatim_a51fee94" ON "gbif_occurrence_csv_verbatim" ("_order");
CREATE INDEX "gbif_occurrence_csv_verbatim_0d3fda0b" ON "gbif_occurrence_csv_verbatim" ("family");
CREATE INDEX "gbif_occurrence_csv_verbatim_030e7a0c" ON "gbif_occurrence_csv_verbatim" ("genus");
CREATE INDEX "gbif_occurrence_csv_verbatim_e94bed27" ON "gbif_occurrence_csv_verbatim" ("specific_epithet");
CREATE INDEX "gbif_occurrence_csv_verbatim_afe8fbda" ON "gbif_occurrence_csv_verbatim" ("kingdom_id");
CREATE INDEX "gbif_occurrence_csv_verbatim_340cabd4" ON "gbif_occurrence_csv_verbatim" ("phylum_id");
CREATE INDEX "gbif_occurrence_csv_verbatim_301e3c17" ON "gbif_occurrence_csv_verbatim" ("class_id");
CREATE INDEX "gbif_occurrence_csv_verbatim_69dfcb07" ON "gbif_occurrence_csv_verbatim" ("order_id");
CREATE INDEX "gbif_occurrence_csv_verbatim_0caa70f7" ON "gbif_occurrence_csv_verbatim" ("family_id");
CREATE INDEX "gbif_occurrence_csv_verbatim_92319714" ON "gbif_occurrence_csv_verbatim" ("genus_id");
CREATE INDEX "gbif_occurrence_csv_verbatim_1699a6e9" ON "gbif_occurrence_csv_verbatim" ("species_id");
CREATE INDEX "gbif_occurrence_csv_verbatim_28c1e37e" ON "gbif_occurrence_csv_verbatim" ("latitude");
CREATE INDEX "gbif_occurrence_csv_verbatim_ba569b80" ON "gbif_occurrence_csv_verbatim" ("longitude");
CREATE INDEX "gbif_occurrence_csv_verbatim_84cdc76c" ON "gbif_occurrence_csv_verbatim" ("year");
CREATE INDEX "gbif_occurrence_csv_verbatim_7436f942" ON "gbif_occurrence_csv_verbatim" ("month");
CREATE INDEX "gbif_occurrence_csv_verbatim_2650cd64" ON "gbif_occurrence_csv_verbatim" ("event_date");
CREATE INDEX "gbif_occurrence_csv_verbatim_scientific_name_12c8f74e_like" ON "gbif_occurrence_csv_verbatim" ("scientific_name" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_verbatim_kingdom_884f3ea5_like" ON "gbif_occurrence_csv_verbatim" ("kingdom" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_verbatim_phylum_75cccab6_like" ON "gbif_occurrence_csv_verbatim" ("phylum" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_verbatim__class_9d1229ac_like" ON "gbif_occurrence_csv_verbatim" ("_class" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_verbatim__order_2f9cdd12_like" ON "gbif_occurrence_csv_verbatim" ("_order" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_verbatim_family_090b86a2_like" ON "gbif_occurrence_csv_verbatim" ("family" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_verbatim_genus_6d31d0ad_like" ON "gbif_occurrence_csv_verbatim" ("genus" text_pattern_ops);
CREATE INDEX "gbif_occurrence_csv_verbatim_specific_epithet_f3b164e4_like" ON "gbif_occurrence_csv_verbatim" ("specific_epithet" text_pattern_ops);
COMMIT;