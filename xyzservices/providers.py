import importlib.resources
import os, sys

from . import provider_sources
from .lib import _load_json

data = os.path.join(sys.prefix, "share", "xyzservices", "providers.json")

if os.path.exists(data):
    with open(data, "r") as f:
        json = f.read()
else:
    json = importlib.resources.read_text(
        provider_sources, "leaflet-providers-parsed.json"
    )

providers = _load_json(json)
