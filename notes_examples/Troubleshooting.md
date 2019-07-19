# Common troubleshooting

## The Postgis service does not initialise 
This could be due to the permissions of the mounting system.


### Manual solution

#### Run postgis backend container
## Use the following command to run the Postgis backend.

```
docker run \
    --name=postgis \
    --network=biospytial_network \
    -it \
    --publish=5432:5432 \
    --volume=[postgis_data_PATH]:/DataVolumes \
    molgor/postgis_biospytial \
    /bin/bash
```

When running, login to the postgis repository

```
docker exec -it [postgis_container] bash
```

Inside the container, change the permissions to:

```
chown -R postgres:postgres /DataVolumes/datadb
```

Todo: create automatic script to solve this issue.



