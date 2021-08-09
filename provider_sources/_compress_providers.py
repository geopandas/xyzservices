"""
This script takes both provider sources stored in `provider_sources`, removes items
which do not represent actual providers (metadata from leaflet-providers-parsed and
templates from xyzservices-providers), combines them together and saves as a compressed
JSON to data/providers.json.

The compressed JSON is shipped with the package.
"""

import json
import warnings

# list of providers known to be broken and should be marked as broken in the JSON
# last update: 8 Aug 2021
BROKEN_PROVIDERS = [
    "OpenPtMap",  # service doesn't exist anymore
    "Hydda.Full",  # down https://github.com/leaflet-extras/leaflet-providers/issues/351
    "Hydda.Base",
    "Hydda.RoadsAndLabels",
    "nlmaps.luchtfoto",  # service phased out
    "NASAGIBS.ModisTerraSnowCover",  # not sure why but doesn't work
]

with open("./leaflet-providers-parsed.json", "r") as f:
    leaflet = json.load(f)
    # remove meta data
    leaflet.pop("_meta", None)


with open("./xyzservices-providers.json", "r") as f:
    xyz = json.load(f)
    # remove templates
    xyz.pop("single_provider_name")
    xyz.pop("provider_bunch_name")


for provider in BROKEN_PROVIDERS:
    provider = provider.replace(".", " ").split()
    try:
        if len(provider) == 1:
            leaflet[provider[0]]["status"] = "broken"
        else:
            leaflet[provider[0]][provider[1]]["status"] = "broken"
    except:
        warnings.warn(
            f"Attempt to mark {provider} as broken failed. "
            "The provider does not exist in leaflet-providers JSON.",
            UserWarning,
        )

# combine both

for key, val in xyz.items():
    if key in leaflet:
        if any(
            isinstance(i, dict) for i in leaflet[key].values()
        ):  # for related group of bunch
            leaflet[key].update(xyz[key])
        else:
            leaflet[key] = xyz[key]
    else:
        leaflet[key] = xyz[key]


with open("../xyzservices/data/providers.json", "w") as f:
    json.dump(leaflet, f, indent=4)
