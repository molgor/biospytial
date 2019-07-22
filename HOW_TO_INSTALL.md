# How to install *Biospytial*

To install the engine you need to have a running [Docker instance (version 1.3 or higher)](https://www.docker.com/get-started) 

The following instructions are tested in a Linux computer.

## Install

1. Download the data from the provided link. [email me if needed](https://ecomorphisms.holobio.me/en/contact/)

2.Modify the file `.env` in the main repository or in `container_files` (It is the same file)
 
 * Change the paths according to the path in your computer where the data was extracted.

## Running the engine 
Run the script:

```
./startEngine.sh
```

 * This file should download the containers and start the services.

## Stoping the engine
Use the script:

```
./stopEngine.sh
```

## Login to Biospytial (Jupyter notebook)
The jupyter notebook is automatically loaded. To access it use a webbrowser and go to the following url:

  *[http://localhost:8888](http://localhost:8888)

If a token is requested run the following command:

```
./getJupyterToken.sh
```
Copy the 
Use the token value and paste it in the webpage.

## Login to Biospytial console
Use the ssh service

```
ssh -p 2323 biospytial@localhost 
```
The password is `biospytial.`

>> It is recommended to change this password if it is intended to use in operational mode.

### Troubleshutting

#### Restart ssh service 
Sometimes the service is not well initialised. Restart the service with:

```
docker exec -it biospytial_client_1 service ssh restart
```


