import immudb_syslog
from immudb_syslog import immudbhandler,logutil,URL
import logging
import json
import os

def _sendfile(filename="/var/log/syslog", collection = "default"):
  log = logging.getLogger('')
  log.setLevel(logging.INFO)

  httpHandler = immudbhandler.ImmudbHttpHandler(
    url=URL + 'default/collection/'+ collection +'/document',
    token=os.environ['IMMUDBKEY'],
    silent=False
  )

  log.addHandler(httpHandler)

  for line in open(filename):
    logging.info(logutil.convert_log(line))
  return immudb_syslog.URL
