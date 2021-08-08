import pytest
import xyzservices.providers as xyz
import requests
import mercantile

flat_free = xyz.filter(requires_token=False).flatten()


def check_provider(provider):
    for key in ["attribution", "name"]:
        assert key in provider.keys()
    assert provider.url.startswith("http")
    for option in ["{z}", "{y}", "{x}"]:
        assert option in provider.url


def get_tile(provider):
    bounds = provider.get("bounds", [[-180, -90], [180, 90]])
    lat = (bounds[0][0] + bounds[1][0]) / 2
    lon = (bounds[0][1] + bounds[1][1]) / 2
    zoom = (provider.get("min_zoom", 0) + provider.get("max_zoom", 20)) // 2
    tile = mercantile.tile(lon, lat, zoom)
    z = tile.z
    x = tile.x
    y = tile.y
    return (z, x, y)


def get_response(url):
    s = requests.Session()
    a = requests.adapters.HTTPAdapter(max_retries=3)
    s.mount("http://", a)
    s.mount("https://", a)
    r = s.get(url)
    return r.status_code


@pytest.mark.parametrize("provider_name", xyz.flatten())
def test_minimal_provider_metadata(provider_name):
    provider = xyz.flatten()[provider_name]
    check_provider(provider)


@pytest.mark.parametrize("name", flat_free)
def test_free_providers(name):
    provider = flat_free[name]

    if provider.get("status"):
        pytest.xfail("Provider is known to be broken.")

    z, x, y = get_tile(provider)

    try:
        r = get_response(provider.build_url(z=z, x=x, y=y))
        assert r == requests.codes.ok
    except AssertionError as e:
        if r == 403:
            pytest.xfail("Provider not available due to API restrictions (Error 403).")

        elif r == 503:
            pytest.xfail("Service temporarily unavailable (Error 503).")

        elif r == 502:
            pytest.xfail("Bad Gateway (Error 502).")

        # check another tiles
        elif r == 404:
            # in some cases, the computed tile is not availble. trying known tiles.
            options = [(12, 2154, 1363), (6, 13, 21), (16, 33149, 22973)]
            results = []
            for o in options:
                z, x, y = o
                r = get_response(provider.build_url(z=z, x=x, y=y))
                results.append(r)
            if not any([x == requests.codes.ok for x in results]):
                raise ValueError(f"Response code: {r}")
        else:
            raise ValueError(f"Response code: {r}")
