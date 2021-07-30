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


def test_expect_name_url_attribution():
    msg = (
        "The attributes `name`, `url`, and `attribution` are "
        "required to initialise a `TileProvider`. Please provide "
        "values for: "
    )
    with pytest.raises(AttributeError, match=msg + "`name`, `url`, `attribution`"):
        TileProvider({})
    with pytest.raises(AttributeError, match=msg + "`url`, `attribution`"):
        TileProvider({"name": "myname"})
    with pytest.raises(AttributeError, match=msg + "`attribution`"):
        TileProvider({"url": "my_url", "name": "my_name"})


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

    required_token = TileProvider(
        {
            "url": "https://myserver.com/tiles/{z}/{x}/{y}_{api_token}.png",
            "attribution": "(C) xyzservices",
            "name": "my_private_provider",
            "api_token": "<insert your API token here>",
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

    expected = "https://myserver.com/tiles/{z}/{x}/{y}_my_token.png"
    assert required_token.build_url(api_token="my_token") == expected

    with pytest.raises(ValueError, match="Token is required for this provider"):
        required_token.build_url()


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


def test_copy():
    basic = TileProvider(
        {
            "url": "https://myserver.com/tiles/{z}/{x}/{y}.png",
            "attribution": "(C) xyzservices",
            "name": "my_public_provider",
        }
    )
    basic2 = basic.copy()
    assert isinstance(basic2, TileProvider)


def test_callable():
    # only testing the callable functionality to override a keyword, as we
    # cannot test the actual providers that need an API key
    updated_provider = xyz.GeoportailFrance.plan(apikey="mykey")
    assert isinstance(updated_provider, TileProvider)
    assert "url" in updated_provider
    assert updated_provider["apikey"] == "mykey"
    # check that original provider dict is not modified
    assert xyz.GeoportailFrance.plan["apikey"] == "choisirgeoportail"
