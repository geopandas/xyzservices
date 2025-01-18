"""
This script takes both provider sources stored in `provider_sources`, removes items
which do not represent actual providers (metadata from leaflet-providers-parsed and
templates from xyzservices-providers), combines them together and saves as a compressed
JSON to data/providers.json.

The compressed JSON is shipped with the package.
"""

import json
import warnings
from datetime import date

import requests
import xmltodict

# list of providers known to be broken and should be marked as broken in the JSON
# last update: 4 Feb 2024
BROKEN_PROVIDERS = [
    "JusticeMap.income",
    "JusticeMap.americanIndian",
    "JusticeMap.asian",
    "JusticeMap.black",
    "JusticeMap.hispanic",
    "JusticeMap.multi",
    "JusticeMap.nonWhite",
    "JusticeMap.white",
    "JusticeMap.plurality",
    "NASAGIBS.ModisTerraChlorophyll",
    "HEREv3.trafficFlow",
    "Stadia.AlidadeSatellite",
]

with open("./leaflet-providers-parsed.json") as f:
    leaflet = json.load(f)
    # remove meta data
    leaflet.pop("_meta", None)


with open("./xyzservices-providers.json") as f:
    xyz = json.load(f)

for provider in BROKEN_PROVIDERS:
    provider = provider.split(".")
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


# update year
def update_year(provider_or_tile):
    if "attribution" in provider_or_tile:
        provider_or_tile["attribution"] = provider_or_tile["attribution"].replace(
            "{year}", str(date.today().year)
        )
        provider_or_tile["html_attribution"] = provider_or_tile[
            "html_attribution"
        ].replace("{year}", str(date.today().year))
    else:
        for tile in provider_or_tile.values():
            update_year(tile)


update_year(xyz)

# combine both

for key, _val in xyz.items():
    if key in leaflet:
        if any(
            isinstance(i, dict) for i in leaflet[key].values()
        ):  # for related group of bunch
            leaflet[key].update(xyz[key])
        else:
            leaflet[key] = xyz[key]
    else:
        leaflet[key] = xyz[key]


# Add IGN WMTS services (Tile images)

ign_wmts_url = (
    "https://data.geopf.fr/wmts?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetCapabilities"
)

response = requests.get(ign_wmts_url)
response_dict = xmltodict.parse(response.content)
layers_list = response_dict["Capabilities"]["Contents"]["Layer"] # 556 layers

wmts_layers_list = []
for i in range(len(layers_list)):
    layer = response_dict["Capabilities"]["Contents"]["Layer"][i]
    variant = layer.get("ows:Identifier")

    # Rename for better readability
    name = ""
    if "." not in variant:
        name = variant.lower().capitalize()
    else:
        name = variant.split(".")[0].lower().capitalize()
        for i in range(1, len(variant.split("."))):
            name = name + "_" + (variant.split(".")[i]).lower().capitalize()
            name = name.replace("-", "_")

    # Rename for better readability (Frequent cases)
    variant_to_name = {
        "CADASTRALPARCELS.PARCELLAIRE_EXPRESS": "parcels",
        "GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2": "plan",
        "ORTHOIMAGERY.ORTHOPHOTOS": "orthos"
    }

    if variant in variant_to_name:
        name = variant_to_name[variant]

    # Get layer style
    style = layer.get("Style")
    if isinstance(style, dict):
        style = style.get("ows:Identifier")

    elif isinstance(style, list):
        style = style[1].get("ows:Identifier") if len(style) > 1 else None
    else:
        style = "normal"

    # Resolution levels (pyramid)
    TileMatrixSet = layer["TileMatrixSetLink"]["TileMatrixSet"]

    # Zoom levels
    TileMatrixSetLimits = layer["TileMatrixSetLink"]["TileMatrixSetLimits"][
        "TileMatrixLimits"
    ]
    min_zoom = int(TileMatrixSetLimits[0]["TileMatrix"])
    max_zoom = int(TileMatrixSetLimits[-1]["TileMatrix"])

    # Tile format
    output_format = layer.get("Format") # image/png...
    if output_format == "application/x-protobuf" or output_format == "image/x-bil;bits=32":
        continue

    # Layer extent
    bbox_lower_left = layer["ows:WGS84BoundingBox"][
        "ows:LowerCorner"
    ]  # given with lon/lat order
    bbox_upper_right = layer["ows:WGS84BoundingBox"][
        "ows:UpperCorner"
    ]  # given with lon/lat order
    lower_left_corner_lon, lower_left_corner_lat = bbox_lower_left.split(
        " "
    )
    upper_right_corner_lon, upper_right_corner_lat = bbox_upper_right.split(
        " "
    )
    bounds = [
        [float(lower_left_corner_lat), float(lower_left_corner_lon)],
        [float(upper_right_corner_lat), float(upper_right_corner_lon)],
    ]

    wmts_layers_list.append("GeoportailFrance." + name)
    leaflet["GeoportailFrance"][name] = {
        "url": """https://data.geopf.fr/wmts?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}""",
        "html_attribution": """<a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a>""",
        "attribution": "Geoportail France",
        "bounds": bounds,
        "min_zoom": min_zoom,
        "max_zoom": max_zoom,
        "format": output_format,
        "style": style,
        "variant": variant,
        "name": "GeoportailFrance." + name,
        "TileMatrixSet": TileMatrixSet,
        "apikey": "your_api_key_here",
    }

    # Handle broken providers
    possibly_broken_providers = [
        "Ocsge_Constructions_2002",
        "Ocsge_Constructions_2014",
        "Orthoimagery_Orthophotos_Coast2000",
        "Ocsge_Couverture_2002",
        "Ocsge_Couverture_2014",
        "Ocsge_Usage_2002",
        "Ocsge_Usage_2014",
        "Pcrs_Lamb93",
        "Geographicalgridsystems_Planignv2_L93",
        "Cadastralparcels_Parcellaire_express_L93",
        "Hr_Orthoimagery_Orthophotos_L93",
        "Raster_zh_centrevdl",
        "Raster_zh_centrevdl_et_auvergnera",
        "Raster_zone_humide_ara_cvdl",
        "Raster_zone_humide_auvergnera",
    ]

    if name in possibly_broken_providers:
        leaflet["GeoportailFrance"][name]["status"] = "broken"

with open("../xyzservices/data/providers.json", "w") as f:
    json.dump(leaflet, f, indent=4)
