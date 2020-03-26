# Ingest *Worldclim2* data into the Relational Processing Unit (RPU)
Juan Escamilla-Molgora, March 2020

The climatic data used in the worked example were obtained from WorldClim2 (Fick and Hijmans, 2017).
The license restricts the redistribution of this dataset and it is necessary to download and install it separately.

## Download data sources
The data need to be downloaded from the project's website. Here we show the direct downloads to the highest resolution datasets (30s). The procedure for lower resolution data is exactly the same.

* [Maximum temperature](http://biogeo.ucdavis.edu/data/worldclim/v2.0/tif/base/wc2.0_30s_tmax.zip)
* [Minimum temperature](http://biogeo.ucdavis.edu/data/worldclim/v2.0/tif/base/wc2.0_30s_tmin.zip)
* [Mean temperature](http://biogeo.ucdavis.edu/data/worldclim/v2.0/tif/base/wc2.0_30s_tmean.zip)
* [Precipitation](http://biogeo.ucdavis.edu/data/worldclim/v2.0/tif/base/wc2.0_30s_prec.zip)
* [Solar Radiation](http://biogeo.ucdavis.edu/data/worldclim/v2.0/tif/base/wc2.0_30s_srad.zip)
* [Wind speed](http://biogeo.ucdavis.edu/data/worldclim/v2.0/tif/base/wc2.0_30s_wind.zip)
* [Vapor pressure](http://biogeo.ucdavis.edu/data/worldclim/v2.0/tif/base/wc2.0_30s_vapr.zip)

The obtained zip files need to be accessible inside the Biospytial client container. 
To do this we can simply copy them to the shared mounting point. 
Typically the folder `/RawDataCSV`.
Check the `container_files/biopytial_stack.yml` to see the host's path.

## Data preparation
Once the datasets (zip files) are accessible (inside Biospytial) we can log into the system, that is, the Biospytial Computing Engine, (client). 
We can do this directly using the docker commands.

`docker exec -it biospytial_stack_client_1 bash`

>> This method logs directly into the ipython console. We need to type `exit` as the ingestion scripts need to be run on Bash.

Or using the SSH service:
`ssh -p 2323 biospytial@localhost`

>> This method logs into biospytial as the user *biospytial* . However, the scripts for ingesting the datasets need to be run as root therefore it is necessary to log as superuser once inside the biospytial client. (i.e. 'sudo -s')

1. Copy the file `multiband_raster_migrateToPostgis.bash` located  in:
`raster_api/bash_raster_tools/bash_scripts`

2. Extract the content of each dataset into a folder with the same name as the data set.
E.g. if the dataset is named: `wc2.0_30s_prec.zip` extract the content into the folder 
`wc2.0_30s_prec`. This can be done with:
`zip -d wc2.0_30s_prec wc2.0_30s_prec.zip`

3. Run the script as:
`bash multiband_raster_migrateToPostgis.bash wc2.0_30s_prec`
This script will transform the *tif* file into an SQL file. 

4. Once the transformation has been done, type the database password to ingest the 
table into the database. By default this password is: `biospytial.`

5. Perform step 2 and 4 for each dataset.

## Notes
This process can take several hours depending on the computer's capacity and the size of the datasets. The SQL files are significantly larger than the original *tif* files. However, once
these files have been ingested into the database they can be removed. 
`rm *.sql`


## References
Fick, S.., Hijmans, R.., 2017. Worldclim 2: New 1-km spatial resolution climate surfaces for global land areas. Int. J. Climatol. doi:10.1002/joc.5086
