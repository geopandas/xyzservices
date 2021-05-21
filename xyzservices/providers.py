from .lib import _load_json

JSON_PATH = "provider_sources/leaflet-providers-parsed.json"

providers = _load_json(JSON_PATH)
