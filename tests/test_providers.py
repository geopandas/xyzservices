import pytest

import xyzservices.providers as xyz


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
