# Using tile providers with other libraries

Folium, ipyleaflet, and Bokeh all accept a `TileProvider` directly.
For example, select the OpenStreetMap basemap once and pass it to any of
the maps below. Each library reads the tile URL and attribution from the
provider.

```python
import xyzservices.providers as xyz

provider = xyz.OpenStreetMap.Mapnik
```

## Folium

Pass the provider as `tiles` when creating a map. Save the result to share
an interactive HTML map.

```python
import folium

m = folium.Map(location=(51.5, -0.1), zoom_start=10, tiles=provider)
m.save("london.html")
```

## ipyleaflet

In a Jupyter notebook, use `basemap` to set the background of the map widget.

```python
from ipyleaflet import Map

Map(center=(51.5, -0.1), zoom=10, basemap=provider)
```

## Bokeh

Use Mercator axes for a tile plot. The axis ranges below are in Web Mercator
meters and cover central London.

```python
from bokeh.plotting import figure, show

p = figure(x_axis_type="mercator", y_axis_type="mercator",
           x_range=(-20000, 0), y_range=(6700000, 6720000))
p.add_tile(provider)
show(p)
```
