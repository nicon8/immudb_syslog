# __main__.py

import sys
import argparse
from immudb_syslog import reader,server

def main():
  parser = argparse.ArgumentParser(prog="immulog",description="log sender to Immudb vault")

  group = parser.add_mutually_exclusive_group()
  group.add_argument("-f", "--file", help="read from file")
  group.add_argument("-s", "--server",action="store_true",help="start syslog server")

  serverargs = parser.add_argument_group("server argument")
  serverargs.add_argument("-p", "--serverport", help="listening port (priviliged ports < 1024 needs admin permission) - default 1514", type=int, default=1514)
  serverargs.add_argument("-l","--serverlisten", help="listening from (specify 0.0.0.0 to listen from all sources) - default 127.0.0.1", default="127.0.0.1")

  generalargs = parser.add_argument_group("general argument")
  generalargs.add_argument("-c","--collection", help="immudb collection to use", default="default")
  args = parser.parse_args()

  if args.file != None:
    reader._sendfile(filename=args.file,collection=args.collection)
  else:
    server._start(server=args.server, port=args.serverport, listen=args.serverlisten, collection = args.collection)

if __name__ == "__main__":
    main()
