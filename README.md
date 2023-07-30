


docker run --mount type=bind,source=/var/log/,target=/var/log immudb_syslog python3  -m immudb_syslog -f /var/log/kern.log -c default


docker run -t -p 1514:1514/udp immudb_syslog python3  -m immudb_syslog -s -l 0.0.0.0 -p 1514 -c syslog
