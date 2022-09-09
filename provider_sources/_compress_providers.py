"""
This script takes both provider sources stored in `provider_sources`, removes items
which do not represent actual providers (metadata from leaflet-providers-parsed and
templates from xyzservices-providers), combines them together and saves as a compressed
JSON to data/providers.json.

The compressed JSON is shipped with the package.
"""

import json
import warnings
import requests
import xmltodict

# list of providers known to be broken and should be marked as broken in the JSON
# last update: 14 Apr 2022
BROKEN_PROVIDERS = []

with open("./leaflet-providers-parsed.json", "r") as f:
    leaflet = json.load(f)
    # remove meta data
    leaflet.pop("_meta", None)


with open("./xyzservices-providers.json", "r") as f:
    xyz = json.load(f)

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


# add the IGN tile layers

leaflet["GeoportailFrance"]["plan"] = {}
leaflet["GeoportailFrance"]["orthos"] = {}
leaflet["GeoportailFrance"]["parcels"] = {}
tilelayers_list = []
apikey_list = [
    "administratif",
    "agriculture",
    "altimetrie",
    "cartes",
    "clc",
    "economie",
    "environnement",
    "essentiels",
    "lambert93",
    "ocsge",
    "ortho",
    "orthohisto",
    "satellite",
    "sol",
    "topographie",
    "transports",
]
url_template = (
    "https://wxs.ign.fr/apikey/geoportail/wmts?REQUEST=GetCapabilities&SERVICE=wmts"
)
for j in range(0, len(apikey_list)):
    apikey = apikey_list[j]
    url = url_template.replace("apikey", apikey)
    resp = requests.get(url)
    resp_dict = xmltodict.parse(resp.content)
    layer_list = resp_dict["Capabilities"]["Contents"]["Layer"]
    addictionnal_dict = {}

    for i in range(len(layer_list)):
        layer = resp_dict["Capabilities"]["Contents"]["Layer"][i]
        variant = layer["ows:Identifier"]
        name = ""
        if "." not in variant:
            name = variant.lower().capitalize()
        else:
            name = variant.split(".")[0].lower().capitalize()
            for i in range(1, len(variant.split("."))):
                name = name + "_" + (variant.split(".")[i]).lower().capitalize()
                name = name.replace("-", "_")

        if variant == "GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2":
            name = "plan"
        if variant == "ORTHOIMAGERY.ORTHOPHOTOS":
            name = "orthos"
        if variant == "CADASTRALPARCELS.PARCELLAIRE_EXPRESS":
            name = "parcels"

        if "Style" in layer.keys():
            if type(layer["Style"]) is dict:
                style = layer["Style"]["ows:Identifier"]

            elif type(layer["Style"]) is list:
                style = layer["Style"][1]["ows:Identifier"]
        else:
            style = "normal"

        TileMatrixSetLimits = layer["TileMatrixSetLink"]["TileMatrixSetLimits"][
            "TileMatrixLimits"
        ]
        min_zoom = int((TileMatrixSetLimits[0]["TileMatrix"]))
        max_zoom = int((TileMatrixSetLimits[-1]["TileMatrix"]))
        TileMatrixSet = layer["TileMatrixSetLink"]["TileMatrixSet"]
        format = layer["Format"]
        bounding_lowerleft_corner = layer["ows:WGS84BoundingBox"]["ows:LowerCorner"]# given with lon/lat order
        bounding_upperright_corner = layer["ows:WGS84BoundingBox"]["ows:UpperCorner"]# given with lon/lat order
        lowerleft_corner_lon, lowerleft_corner_lat = bounding_lowerleft_corner.split(" ")
        upperright_corner_lon, upperright_corner_lat = bounding_upperright_corner.split(" ")
        bounds = [[float(lowerleft_corner_lat), float(lowerleft_corner_lon)], [float(upperright_corner_lat), float(upperright_corner_lon)]]

        if format == "application/x-protobuf":
            pass
        elif format == "image/x-bil;bits=32":
            pass
        elif apikey == "lambert93":
            pass
        else:
            tilelayers_list.append("GeoportailFrance." + name)
            leaflet["GeoportailFrance"][name] = {
                "url": """https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}""",
                "html_attribution": """<a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a>""",
                "attribution": "Geoportail France",
                "bounds": bounds,
                "min_zoom": min_zoom,
                "max_zoom": max_zoom,
                "apikey": apikey,
                "format": format,
                "style": style,
                "variant": variant,
                "name": "GeoportailFrance." + name,
                "TileMatrixSet": TileMatrixSet,
            }

with open("../xyzservices/data/providers.json", "w") as f:
    json.dump(leaflet, f, indent=4)
