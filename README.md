Docker for local built bitcoind
============================

This setup based on docker setup in https://github.com/btccom/btcpool

create.py is python script to generate docker image base on the local bitcoind
[Options]
* --repo [reponame]. Set the docker image repo name. Default name bitcoind_local
* --tag [tag]. Set the docker image tag. Default is random string
* --sourcedir [bitcoind directory location]. Copy bitcoind from specified directory. if not specified, it will use ./
* --use-installed. Copy bitcoind based on `which bitcoind`

* OS: `Ubuntu 14.04 LTS`, `Ubuntu 16.04 LTS`
* Docker Image OS: `Ubuntu 16.04 LTS`

## Install Docker

```
# Use 'curl -sSL https://get.daocloud.io/docker | sh' instead of this line
# when your server is in China.
wget -qO- https://get.docker.com/ | sh

service docker start
service docker status
```


## Build Docker Images
Build your bitcoind project like usual

Install python

#examples
create.py 
create.py --sourcedir src/
create.py --repo btc --tag latest --use-installed

## Running docker image

```
cd /work

# mkdir for bitcoin-abc
mkdir -p /work/bitcoin-abc

# bitcoin.conf
touch /work/bitcoin-abc/bitcoin.conf
```

### bitcoin.conf example

```
rpcuser=bitcoinrpc
# generate random rpc password:
#   $ strings /dev/urandom | grep -o '[[:alnum:]]' | head -n 30 | tr -d '\n'; echo
rpcpassword=xxxxxxxxxxxxxxxxxxxxxxxxxx
rpcthreads=4

rpcallowip=172.16.0.0/12
rpcallowip=192.168.0.0/16
rpcallowip=10.0.0.0/8

# use 1G memory for utxo, depends on your machine's memory
dbcache=1000

# use 8MB block when call GBT
# The blockmaxsize should be between 1000001 and 8000000.
blockmaxsize=8000000
```

## Start Docker Container

```
# start docker
docker run -it -v /work/bitcoin-abc:/root/.bitcoin --name bitcoin-abc -p 8333:8333 -p 8332:8332 -p 8331:8331 --restart always -d bitcoin-abc:0.16.1
#docker run -it -v /work/bitcoin-abc:/root/.bitcoin --name bitcoin-abc -p 8333:8333 -p 8332:8332 -p 8331:8331 -p 18333:18333 -p 18332:18332 -p 18331:18331 --restart always -d bitcoin-abc:0.16.1

# login
docker exec -it bitcoin-abc /bin/bash
```
