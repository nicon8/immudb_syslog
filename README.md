# Immudb syslog example

Python modules that store syslog entries on the [immudb vault cloud](https://vault.immudb.io/). The module can work in two different ways:
- **reader**: The module will read a syslog file passed as input, parsing it line by line, and pushing each entry to [immudb vault cloud](https://vault.immudb.io/)
- **server**: The module will run a standalone syslog server that can be used as a remote destination for your current syslog server. Whenever the server receives entries, it will push the entries to the immudb vault cloud [immudb vault cloud](https://vault.immudb.io/)

# Usage

```
usage: immulog [-h] [-f FILE | -s] [-p SERVERPORT] [-l SERVERLISTEN] [-c COLLECTION]

log sender to Immudb vault

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  read from file
  -s, --server          start syslog server

server argument:
  -p SERVERPORT, --serverport SERVERPORT
                        listening port (priviliged ports < 1024 needs admin permission) - default 1514
  -l SERVERLISTEN, --serverlisten SERVERLISTEN
                        listening from (specify 0.0.0.0 to listen from all sources) - default 127.0.0.1

general argument:
  -c COLLECTION, --collection COLLECTION
                        immudb collection to use
```
# Getting started
To run the examples, you'll need a personal key obtained from [immudb vault cloud](https://vault.immudb.io/). The Free plan should be more than sufficient for most use cases.

The immudb key should be passed to the module using the environmental variable "IMMUDBKEY".

The easiest way to use the module is with Docker. There is a predefined Dockerfile available in the repository, which you can use to build the Docker image. This will help you run the module seamlessly within a containerized environment.




## Docker
Clone the repo
```
git clone https://github.com/nicon8/immudb_syslog.git
```
```
#Build docker image
docker build --tag immudb_syslog
```
Once the image is built, there is no need to maintain the docker container during execution. We can directly specify the command inside 'docker run' command.

## Reading from syslog file with Docker

**_NOTE:_** **Remember to change the value of the variable IMMUDBKEY using your personal key obtained from [immudb vault cloud](https://vault.immudb.io/)**

```
IMMUDBKEY=default.xxx
docker run -t -e IMMUDBKEY=$IMMUDBKEY --mount type=bind,source=/var/log/,target=/var/log immudb_syslog python3  -m immudb_syslog -f /var/log/kern.log -c default
```

The --mount option is required in this example to enable the Docker container to access the host system's log file. You can easily modify the example to use any of the different syslog file present in your machine. \
es. in my ubuntu syslog config files are (from /etc/rsyslog.d/50-default.conf):
* /var/log/auth.log
* /var/log/syslog
* /var/log/cron.log
* /var/log/daemon.log
* /var/log/kern.log
* /var/log/lpr.log
* /var/log/mail.log
* /var/log/user.log


## Launch a local standalone syslog server with Docker
**_NOTE:_** **Remember to update the value of the variable IMMUDBKEY with your personal key obtained from [immudb vault cloud](https://vault.immudb.io/)**
```
#Run it as standalone server
PORT=1514
IMMUDBKEY=default.xxx
docker run -t -e IMMUDBKEY=$IMMUDBKEY -p $PORT:$PORT/udp immudb_syslog python3  -m immudb_syslog -s -l 0.0.0.0 -p $PORT -c syslog
```
Once it is running, you can test the server typing in another shell:
```
logger -n 127.0.0.1 -P 1514 -p 1 -t test -d -i -- I'm very important and I want to be store safely
```
The Docker container in this example will map port 1514 to port 1514 on the host system, and it is essential that this port matches the one used by the module's standalone syslog server.

## Python env

Create and activate a new python env
```
IMMUDBENV=~/immudbenv
python3 -m venv ~/immudbenv
source ~/immudbenv/bin/activate
```

Clone the repo
```
git clone https://github.com/nicon8/immudb_syslog.git
```
Install the module locally
```
python3 -m pip install -e .
```
## Reading from syslog file
```
python3 -m immudb_syslog -f "/var/log/syslog"
```
## Launch a local standalone syslog server
```
python3 -m immudb_syslog -s -l "0.0.0.0" -p 1514 -c default
```
Once it is running, you can test the server typing in another shell:
```
logger -n 127.0.0.1 -P 1514 -p 1 -t test -d -i -- I'm very important and I want to be store safely
```
## Credits
[Immudb Vault API Reference](https://vault.immudb.io/docs/api/v1)\
[Tiny syslog server in python](https://gist.github.com/marcelom/4218010)\
[Syslog parsing in python](https://gist.github.com/leandrosilva/3651640)\
[Custom HTTP Handler for logging](https://stackoverflow.com/questions/51525237/how-to-set-up-httphandler-for-python-logging)

## TODO
* Implement complete error handling (e.g., handling missing collections, missing files, etc.).
* Handle collection creation.
* Rewrite the Syslog Parser.
