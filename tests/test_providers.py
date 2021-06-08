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


def test_requires_token():
    private_provider = TileProvider(
        {
            "url": "https://myserver.com/tiles/{z}/{x}/{y}?access_token={accessToken}",
            "attribution": "(C) xyzservices",
            "accessToken": "<insert your access token here>",
            "name": "my_private_provider",
        }
    )

    public_provider = TileProvider(
        {
            "url": "https://myserver.com/tiles/{z}/{x}/{y}",
            "attribution": "(C) xyzservices",
            "name": "my_public_provider",
        }
    )

    assert private_provider.requires_token() == True
    assert public_provider.requires_token() == False
