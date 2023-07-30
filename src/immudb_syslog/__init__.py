# __init__.py

from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

__version__ = "0.0.1"

# Read URL of the Real Python feed from config file
#print(resources.read_text("immudb_syslog", "config.toml"))
cfg = tomllib.loads(resources.read_text("immudb_syslog", "config.toml"))

URL = cfg["immudb"]["url"]
