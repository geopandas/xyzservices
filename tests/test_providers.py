import pytest

import xyzservices.providers as xyz
from xyzservices import TileProvider


def check_provider(provider):
    for key in ["attribution", "name"]:
        assert key in provider.keys()
    assert provider.url.startswith("http")
    for option in ["{z}", "{y}", "{x}"]:
        assert option in provider.url


@pytest.mark.parametrize("provider_name", xyz.keys())
def test_minimal_provider_metadata(provider_name):
    provider = xyz[provider_name]

    if "url" in provider.keys():
        check_provider(provider)

    else:
        for variant in xyz[provider_name]:
            check_provider(xyz[provider_name][variant])


def test_build_url():
    basic = TileProvider(
        {
            "url": "https://myserver.com/tiles/{z}/{x}/{y}.png",
            "attribution": "(C) xyzservices",
            "name": "my_public_provider",
        }
    )
    retina = TileProvider(
        {
            "url": "https://myserver.com/tiles/{z}/{x}/{y}{r}.png",
            "attribution": "(C) xyzservices",
            "name": "my_public_provider",
            "r": "@2x",
        }
    )

    silent_retina = TileProvider(
        {
            "url": "https://myserver.com/tiles/{z}/{x}/{y}{r}.png",
            "attribution": "(C) xyzservices",
            "name": "my_public_provider",
        }
    )

    expected = "https://myserver.com/tiles/{z}/{x}/{y}.png"
    assert basic.build_url() == expected

    expected = "https://myserver.com/tiles/3/1/2.png"
    assert basic.build_url(1, 2, 3) == expected
    assert basic.build_url(1, 2, 3, scale_factor="@2x") == expected
    assert silent_retina.build_url(1, 2, 3) == expected

    expected = "https://myserver.com/tiles/3/1/2@2x.png"
    assert retina.build_url(1, 2, 3) == expected
    assert silent_retina.build_url(1, 2, 3, scale_factor="@2x") == expected

    expected = "https://myserver.com/tiles/3/1/2@5x.png"
    assert retina.build_url(1, 2, 3, scale_factor="@5x") == expected
