# Immudb syslog example

Python modules which stores syslog entries on [immudb vault cloud](https://vault.immudb.io/). The module can work in two different ways:
- **reader**: the module will read line by line a syslog file passed as input, parse line by line, and push entry by entry to immudb vault cloud](https://vault.immudb.io/)
- **server**: the module will run a standalone syslog server which can be used as a remote destination for your current syslog server. Whenever the server receive an entries, it will push the entry to immudb vault cloud](https://vault.immudb.io/)

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
To run the examples, you need a personal key obtained from [immudb vault cloud](https://vault.immudb.io/). Free plan is more than enough.
The immudb key is passed to the module using the environmental variable "IMMUDBKEY"

The easiest way to use the module is using docker. A predefined Dockerfile is in the repo.

## Docker
Clone the repo
```
git clone https://github.com/nicon8/immudb_syslog.git
```
```
#Build docker image
docker build --tag immudb_syslog
```
Once image is built, there is no need to maintain the docker container in execution. We can directly specify the command inside docker run command.

## Reading from syslog file with Docker

**_NOTE:_** **Remember to change the value of the variable IMMUDBKEY using your personal key obtained from [immudb vault cloud](https://vault.immudb.io/)**

```
IMMUDBKEY=default.xxx
docker run -t -e IMMUDBKEY=$IMMUDBKEY --mount type=bind,source=/var/log/,target=/var/log immudb_syslog python3  -m immudb_syslog -f /var/log/kern.log -c default
```

The --mount option is needed in this example to allow the Docker container to find the host system file logs. You can easily change the example using one of the different syslog file present in your machine. \
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
**_NOTE:_** **Remember to change the value of the variable IMMUDBKEY using your personal key obtained from [immudb vault cloud](https://vault.immudb.io/)**
```
#Run it as standalone server
PORT=1514
IMMUDBKEY=default.xxx
docker run -t -e IMMUDBKEY=$IMMUDBKEY -p $PORT:$PORT/udp immudb_syslog python3  -m immudb_syslog -s -l 0.0.0.0 -p $PORT -c syslog
```
Once it is running, to test the server you can type on another shell:
```
logger -n 127.0.0.1 -P 1514 -p 1 -t test -d -i -- I'm very important and I want to be store safely
```

The docker container in this example will map port 1514 to port 1514 on the host system, and this has to be the same port used by the module standalone syslog server.

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
Once it is running, to test the server you can type on another shell:
```
logger -n 127.0.0.1 -P 1514 -p 1 -t test -d -i -- I'm very important and I want to be store safely
```
## Credits
[Immudb Vault API Reference](https://vault.immudb.io/docs/api/v1)\
[Tiny syslog server in python](https://gist.github.com/marcelom/4218010)\
[Syslog parsing in python](https://gist.github.com/leandrosilva/3651640)\
[Custom HTTP Handler for logging](https://stackoverflow.com/questions/51525237/how-to-set-up-httphandler-for-python-logging)

## TODO
* Complete error handling (missing collection, missing file, ..)
* Manage collection creation
* Syslog Parser to rewrite
