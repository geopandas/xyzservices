# Providers requiring registration

The main group of providers is retrieved from the [`leaflet-providers`
project](https://github.com/leaflet-extras/leaflet-providers) that contains both openly
accessible providers as well as those requiring registration. All of them are considered
[free](https://github.com/leaflet-extras/leaflet-providers/blob/master/README.md#what-do-we-mean-by-free).

Below is the (potentially incomplete) list of providers requiring registration.

```{note}
This page is largely taken directly from the [`leaflet-providers` project](https://github.com/leaflet-extras/leaflet-providers/blob/master/README.md).
```

## Esri/ArcGIS

In order to use ArcGIS maps, you must
[register](https://developers.arcgis.com/en/sign-up/) and abide by the [terms of
service](https://developers.arcgis.com/en/terms/). No special syntax is required.

## Geoportail France

In order to use Geoportail France resources, you need to obtain an [api
key](http://professionnels.ign.fr/ign/contrats/) that allows you to access the
[resources](https://geoservices.ign.fr/documentation/donnees-ressources-wmts.html#ressources-servies-en-wmts-en-projection-web-mercator)
you need. Pass this api key to the `TileProvider`:

```py
xyz.GeoportailFrance.plan(apikey="<insert api_key here>")
```

Please note that a public api key (`choisirgeoportail`) is used by default and comes
with no guarantee.

## HERE and HEREv3 (formerly Nokia)

In order to use HEREv3 layers, you must [register](http://developer.here.com/). Once
registered, you can create an `apiKey` which you have to pass to the `TileProvider`:

```py
# Overriding the attribute will alter the existing object
xyz.HEREv3.terrainDay["apiKey"] = "my-private-api-key"

# Calling the object will return a copy
xyz.HEREv3.terrainDay(apiKey="my-private-api-key")
```

You can still pass `app_id` and `app_code` in legacy projects:

```py
xyz.HERE.terrainDay(app_id="my-private-app-id", app_code="my-app-code")
```

## Jawg Maps

In order to use Jawg Maps, you must [register](https://www.jawg.io/lab). Once
registered, your access token will be located
[here](https://www.jawg.io/lab/access-tokens) and you will access to all Jawg default
maps (variants) and your own customized maps:

```py
xyz.Jawg.Streets(
    accessToken="<insert access token here>",
    variant="<insert map id here or blank for default variant>"
)
```

## Mapbox

In order to use Mapbox maps, you must [register](https://tiles.mapbox.com/signup). You
can get map_ID (e.g. `"mapbox/satellite-v9"`) and `ACCESS_TOKEN` from [Mapbox
projects](https://www.mapbox.com/projects):

```py
xyz.MapBox(id="<insert map_ID here>", accessToken="my-private-ACCESS_TOKEN")
```

The currently-valid Mapbox map styles, to use for map_IDs, [are listed in the Mapbox
documentation](https://docs.mapbox.com/api/maps/#mapbox-styles) - only the final part of
each is required, e.g. `"mapbox/light-v10"`.

## MapTiler Cloud

In order to use MapTiler maps, you must [register](https://cloud.maptiler.com/). Once
registered, get your API key from Account/Keys, which you have to pass to the
`TileProvider`:

```py
xyz.MapTiler.Streets(key="<insert key here>")
```

## Thunderforest

In order to use Thunderforest maps, you must
[register](https://thunderforest.com/pricing/). Once registered, you have an `api_key`
which you have to pass to the `TileProvider`:

```py
xyz.Thunderforest.Landscape(apikey="<insert api_key here>")
```

## TomTom

In order to use TomTom layers, you must
[register](https://developer.tomtom.com/user/register). Once registered, you can create
an `apikey` which you have to pass to the `TileProvider`:

```py
xyz.TomTom(apikey="<insert api_key here>")
```

## Stadia Maps

In order to use Stadia maps, you must [register](https://client.stadiamaps.com/signup/).
Once registered, you can whitelist your domain within your account settings.

Alternatively, you can use Stadia maps with an API token but you need to adapt a
provider object to correct form.

```py
provider = xyz.Stadia.AlidadeSmooth(api_key="<insert api_key here>")
provider["url"] = provider["url"] + "?api_key={api_key}"  # adding API key placeholder
```

## Ordnance Survey

In order to use Ordnance Survey layers, you must
[register](https://osdatahub.os.uk/). Once registered, you can create
a project, assign OS Maps API product to a project and retrieve the `key` which you have to pass to the `TileProvider`:

```py
xyz.OrdnanceSurvey.Light(key="<insert api_key here>")
```
