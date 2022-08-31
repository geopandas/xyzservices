import requests
import xmltodict
import json

with open('initial_providers.json') as json_file:
    data = json.load(json_file)

data['GeoportailFrance']['plan'] = {}
data['GeoportailFrance']['orthos'] = {}
data['GeoportailFrance']['parcels'] = {}
tilelayers_list = []
apikey_list = ['administratif', 'agriculture', 'altimetrie', 'cartes', 'clc', 'economie', 'environnement', 'essentiels', 'lambert93', 'ocsge', 'ortho', 'orthohisto', 'satellite', 'sol', 'topographie', 'transports']
url_template = 'https://wxs.ign.fr/apikey/geoportail/wmts?REQUEST=GetCapabilities&SERVICE=wmts'
for j in range(0, len(apikey_list)):
    apikey = apikey_list[j]
    url = url_template.replace('apikey', apikey)
    resp = requests.get(url)
    resp_dict = xmltodict.parse(resp.content)
    layer_list = resp_dict['Capabilities']['Contents']['Layer']
    addictionnal_dict = {}

    for i in range(len(layer_list)):
        layer = resp_dict['Capabilities']['Contents']['Layer'][i]
        variant = layer['ows:Identifier']
        name = ''
        if ('.' not in variant):
            name = variant.lower().capitalize()
        else:
            name = variant.split('.')[0].lower().capitalize()
            for i in range(1, len(variant.split('.'))):
                name = name + '_' + (variant.split('.')[i]).lower().capitalize()
                name = name.replace('-', '_')

        if variant == 'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2':
            name = 'plan'
        if variant == 'ORTHOIMAGERY.ORTHOPHOTOS':
            name = 'orthos'
        if variant == 'CADASTRALPARCELS.PARCELLAIRE_EXPRESS':
            name = 'parcels'

        if 'Style' in layer.keys():
            if type(layer['Style']) is dict :
                style = layer['Style']['ows:Identifier']

            elif type(layer['Style']) is list :
                style = layer['Style'][1]['ows:Identifier']
        else:
            style = 'normal'

        TileMatrixSetLimits = layer['TileMatrixSetLink']['TileMatrixSetLimits']['TileMatrixLimits']
        min_zoom = int((TileMatrixSetLimits[0]['TileMatrix']))
        max_zoom = int((TileMatrixSetLimits[-1]['TileMatrix']))
        TileMatrixSet = layer['TileMatrixSetLink']['TileMatrixSet']
        format = layer['Format']
        bounding_lower_corner = layer['ows:WGS84BoundingBox']['ows:LowerCorner']
        bounding_upper_corner = layer['ows:WGS84BoundingBox']['ows:UpperCorner']
        lower1, lower2 = bounding_lower_corner.split(' ')
        upper1, upper2 = bounding_upper_corner.split(' ')
        bounds = [[float(lower1), float(lower2)], [float(upper1), float(upper2)]]
        for k in range(len(resp_dict['Capabilities']['Contents']['TileMatrixSet'])):
            supportedCRS = resp_dict['Capabilities']['Contents']['TileMatrixSet'][k]['ows:SupportedCRS']

        if (format == 'application/x-protobuf'):
            pass
        elif (format == 'image/x-bil;bits=32'):
            pass
        elif (apikey == 'lambert93'):
            pass
        else:
            tilelayers_list.append("GeoportailFrance." + name)
            data['GeoportailFrance'][name] = {
                "url": "https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}",
                "html_attribution": "<a target=\"_blank\" href=\"https://www.geoportail.gouv.fr/\">Geoportail France</a>",
                "attribution": "Geoportail France",
                "bounds": bounds,
                "min_zoom": min_zoom,
                "max_zoom": max_zoom,
                "apikey": apikey,
                "format": format,
                "style": style,
                "variant": variant,
                "name": "GeoportailFrance." + name,
                "TileMatrixSet": TileMatrixSet
            }

with open('providers.json', 'w') as fp:
    json.dump(data, fp, indent=2)
