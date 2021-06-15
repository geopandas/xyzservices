import pytest

import xyzservices.providers as xyz
from xyzservices import TileProvider, Bunch


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


def test_html_repr():
    provider = TileProvider(
        {
            "url": "https://myserver.com/tiles/{z}/{x}/{y}.png",
            "attribution": "(C) xyzservices",
            "name": "my_public_provider",
        }
    )
    provider2 = TileProvider(
        {
            "url": "https://myserver.com/tiles2/{z}/{x}/{y}.png",
            "attribution": "(C) xyzservices",
            "name": "my_public_provider2",
        }
    )

    provider_strings = [
        '<div class="xyz-wrap">',
        '<div class="xyz-header">',
        '<div class="xyz-obj">xyzservices.TileProvider</div>',
        '<div class="xyz-name">my_public_provider</div>',
        '<div class="xyz-details">',
        '<dl class="xyz-attrs">',
        "<dt><span>url</span></dt><dd>https://myserver.com/tiles/{z}/{x}/{y}.png</dd>",
        "<dt><span>attribution</span></dt><dd>(C) xyzservices</dd>",
    ]

    for html_string in provider_strings:
        assert html_string in provider._repr_html_()

    bunch = Bunch({"first": provider, "second": provider2})

    bunch_strings = [
        '<div class="xyz-obj">xyzservices.Bunch</div>',
        '<div class="xyz-name">2 items</div>',
        '<ul class="xyz-collapsible">',
        '<li class="xyz-child">',
        "<span>xyzservices.TileProvider</span>",
        '<div class="xyz-inside">',
    ]

    bunch_repr = bunch._repr_html_()
    for html_string in provider_strings + bunch_strings:
        assert html_string in bunch_repr
    assert bunch_repr.count('<li class="xyz-child">') == 2
    assert bunch_repr.count('<div class="xyz-wrap">') == 3
    assert bunch_repr.count('<div class="xyz-header">') == 3
