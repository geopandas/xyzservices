"""
This script takes both provider sources stored in `provider_sources`, removes
items which do not represent actual providers (metadata from leaflet-providers-parsed
and templates from xyzservices-providers), combines them together and saves as a compressed
JSON to data/providers.json.

The compressed JSON is shipped with the package.
"""

import json

with open("../provider_sources/leaflet-providers-parsed.json", "r") as f:
    leaflet = json.load(f)
    # remove meta data
    leaflet.pop("_meta", None)

with open("../provider_sources/xyzservices-providers.json", "r") as f:
    xyz = json.load(f)
    # remove templates
    xyz.pop("single_provider_name")
    xyz.pop("provider_bunch_name")


# combine both
leaflet.update(xyz)

with open("./data/providers.json", "w") as f:
    json.dump(leaflet, f)
