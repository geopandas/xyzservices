import importlib.resources

from . import provider_sources
from .lib import _load_json


json = importlib.resources.read_text(provider_sources, "leaflet-providers-parsed.json")

providers = _load_json(json)
