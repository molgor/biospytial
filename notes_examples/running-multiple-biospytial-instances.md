# Running multiple Biospytial instances
Due to its modular architecture, Biospytial can be replicated multiple times to
distribute the workload.


### Instantiate a cluster
For doing so, we need to create a cluster between computers. They need to be connected
in the same network (could be VPN).

```
docker swarm init --advertise-addr <MANAGER-IP>
```

#### [Optional] Label it to assign services to specific nodes
```
docker node update --label-add manager [hostname1]

docker node update --label-add worker1 [hostname2]
```

### To create a new node and add it to the swarm do:
Run the following command on a manager node to retrieve the join command for a worker:
```
docker swarm join-token worker 
```

To add a worker to this swarm, run the following command:

#### Example:
```
docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
  192.168.99.100:2377

```






