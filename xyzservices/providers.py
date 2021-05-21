from pathlib import Path
from .lib import _load_json

# we need to get an absolute path to our JSON
JSON_PATH = (
    str(Path(__file__).parent.parent)
    + "/provider_sources/leaflet-providers-parsed.json"
)

providers = _load_json(JSON_PATH)
