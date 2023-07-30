import logging
import socketserver
from immudb_syslog import immudbhandler,logutil,URL
import json
import os

log = logging.getLogger('')
log.setLevel(logging.INFO)


class SyslogUDPHandler(socketserver.BaseRequestHandler):
  def handle(self):
    data = bytes.decode(self.request[0].strip())
    socket = self.request[1]
    logging.info(logutil.convert_bin_log(str(data)))

def _start(server, port, listen, collection):
  httpHandler = immudbhandler.ImmudbHttpHandler(
    url=URL+'default/collection/'+collection+'/document',
    token=os.environ['IMMUDBKEY'],
    silent=False
  )

  log.addHandler(httpHandler)

  try:
    server = socketserver.UDPServer((listen,port), SyslogUDPHandler)
    server.serve_forever(poll_interval=0.5)
  except (IOError, SystemExit):
    raise
  except KeyboardInterrupt:
    print ("Crtl+C Pressed. Shutting down.")
