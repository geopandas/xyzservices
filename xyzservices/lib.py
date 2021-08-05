"""
Utilities to support XYZservices
"""
import json
import uuid
from typing import Optional


class Bunch(dict):
    """A dict with attribute-access

    :class:`Bunch` is used to store :class:`TileProvider` objects.

    Examples
    --------
    >>> black_and_white = TileProvider(
    ...     name="My black and white tiles",
    ...     url="https://myserver.com/bw/{z}/{x}/{y}",
    ...     attribution="(C) xyzservices",
    ... )
    >>> colorful = TileProvider(
    ...     name="My colorful tiles",
    ...     url="https://myserver.com/color/{z}/{x}/{y}",
    ...     attribution="(C) xyzservices",
    ... )
    >>> MyTiles = Bunch(BlackAndWhite=black_and_white, Colorful=colorful)
    >>> MyTiles
    {'BlackAndWhite': {'name': 'My black and white tiles', 'url': \
'https://myserver.com/bw/{z}/{x}/{y}', 'attribution': '(C) xyzservices'}, 'Colorful': \
{'name': 'My colorful tiles', 'url': 'https://myserver.com/color/{z}/{x}/{y}', \
'attribution': '(C) xyzservices'}}
    >>> MyTiles.BlackAndWhite.url
    'https://myserver.com/bw/{z}/{x}/{y}'
    """

    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __dir__(self):
        return self.keys()

    def _repr_html_(self, inside=False):

        children = ""
        for key in self.keys():
            if isinstance(self[key], TileProvider):
                obj = "xyzservices.TileProvider"
            else:
                obj = "xyzservices.Bunch"
            uid = str(uuid.uuid4())
            children += f"""
            <li class="xyz-child">
                <input type="checkbox" id="{uid}" class="xyz-checkbox"/>
                <label for="{uid}">{key} <span>{obj}</span></label>
                <div class="xyz-inside">
                    {self[key]._repr_html_(inside=True)}
                </div>
            </li>
            """

        style = "" if inside else f"<style>{CSS_STYLE}</style>"
        html = f"""
        <div>
        {style}
            <div class="xyz-wrap">
                <div class="xyz-header">
                    <div class="xyz-obj">xyzservices.Bunch</div>
                    <div class="xyz-name">{len(self)} items</div>
                </div>
                <div class="xyz-details">
                    <ul class="xyz-collapsible">
                        {children}
                    </ul>
                </div>
            </div>
        </div>
        """

        return html

    def flatten(self) -> "Bunch":
        """Return the nested :class:`Bunch` collapsed into one level.

        Note: Formerly nested :class:`TileProvider`s cannot be accessed as attributes
        and have to be accessed via index operator (as in ``flat["OpenStreetMap.Mapnik"]
        not ``flat.OpenStreetMap.Mapnik``).

        Returns
        -------
        flattened : Bunch

        Examples
        --------
        >>> import xyzservices.providers as xyz
        >>> len(xyz)
        36

        >>> flat = xyz.flatten()
        >>> len(xyz)
        207

        """

        flat = Bunch()

        def _get_providers(provider):
            if isinstance(provider, TileProvider):
                flat[provider.name] = provider
            else:
                for prov in provider.values():
                    _get_providers(prov)

        _get_providers(self)

        return flat


class TileProvider(Bunch):
    """
    A dict with attribute-access and that
    can be called to update keys


    Examples
    --------

    You can create custom :class:`TileProvider` by passing your attributes to the object
    as it would have been a ``dict()``. It is required to always specify ``name``,
    ``url``, and ``attribution``.

    >>> public_provider = TileProvider(
    ...     name="My public tiles",
    ...     url="https://myserver.com/tiles/{z}/{x}/{y}.png",
    ...     attribution="(C) xyzservices",
    ... )

    Alternatively, you can create it from a dictionary of attributes. When specifying a
    placeholder for the access token, please use the ``"<insert your access token
    here>"`` string to ensure that :meth:`~xyzservices.TileProvider.requires_token`
    method works properly.

    >>> private_provider = TileProvider(
    ...    {
    ...        "url": "https://myserver.com/tiles/{z}/{x}/{y}.png?apikey={accessToken}",
    ...        "attribution": "(C) xyzservices",
    ...        "accessToken": "<insert your access token here>",
    ...        "name": "my_private_provider",
    ...    }
    ... )

    You can then fetch all information as attributes:

    >>> public_provider.url
    'https://myserver.com/tiles/{z}/{x}/{y}.png'

    >>> public_provider.attribution
    '(C) xyzservices'

    To ensure you will be able to use the tiles, you can check if the
    :class:`TileProvider` requires a token or API key.

    >>> public_provider.requires_token()
    False
    >>> private_provider.requires_token()
    True

    You can also generate URL in the required format with or without placeholders:

    >>> public_provider.build_url()
    'https://myserver.com/tiles/{z}/{x}/{y}.png'
    >>> private_provider.build_url(x=12, y=21, z=11, accessToken="my_token")
    'https://myserver.com/tiles/11/12/21.png?access_token=my_token'

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        missing = []
        for el in ["name", "url", "attribution"]:
            if el not in self.keys():
                missing.append(el)
        if len(missing) > 0:
            msg = (
                f"The attributes `name`, `url`, "
                f"and `attribution` are required to initialise "
                f"a `TileProvider`. Please provide values for: "
                f'`{"`, `".join(missing)}`'
            )
            raise AttributeError(msg)

    def __call__(self, **kwargs):
        new = TileProvider(self)  # takes a copy preserving the class
        new.update(kwargs)
        return new

    def copy(self, **kwargs):
        new = TileProvider(self)  # takes a copy preserving the class
        return new

    def build_url(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        z: Optional[int] = None,
        scale_factor: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Build the URL of tiles from the :class:`TileProvider` object

        Can return URL with placeholders or the final tile URL.

        Parameters
        ----------

        x, y, z : int (optional)
            tile number
        scale_factor : str (optional)
            Scale factor (where supported). For example, you can get double resolution
            (512 x 512) instead of standard one (256 x 256) with ``"@2x"``. If you want
            to keep a placeholder, pass `"{r}"`.

        **kwargs
            Other potential attributes updating the :class:`TileProvider`.

        Returns
        -------

        url : str
            Formatted URL

        Examples
        --------
        >>> import xyzservices.providers as xyz

        >>> xyz.CartoDB.DarkMatter.build_url()
        'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'

        >>> xyz.CartoDB.DarkMatter.build_url(x=9, y=11, z=5)
        'https://a.basemaps.cartocdn.com/dark_all/5/9/11.png'

        >>> xyz.CartoDB.DarkMatter.build_url(x=9, y=11, z=5, scale_factor="@2x")
        'https://a.basemaps.cartocdn.com/dark_all/5/9/11@2x.png'

        >>> xyz.MapBox.build_url(accessToken="my_token")
        'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=my_token'

        """
        provider = self.copy()

        if x is None:
            x = "{x}"
        if y is None:
            y = "{y}"
        if z is None:
            z = "{z}"

        provider.update(kwargs)

        if provider.requires_token():
            raise ValueError(
                "Token is required for this provider, but not provided. "
                "You can either update TileProvider or pass respective keywords "
                "to build_url()."
            )

        url = provider.pop("url")
        subdomains = provider.pop("subdomains", "abc")
        if scale_factor:
            r = scale_factor
            provider.pop("r", None)
        else:
            r = provider.pop("r", "")

        return url.format(x=x, y=y, z=z, s=subdomains[0], r=r, **provider)

    def requires_token(self) -> bool:
        """
        Returns ``True`` if the TileProvider requires access token to fetch tiles.

        The token attribute name vary and some :class:`TileProvider` objects may require
        more than one token (e.g. ``HERE``). The information is deduced from the
        presence of `'<insert your...'` string in one or more of attributes. When
        specifying a placeholder for the access token, please use the ``"<insert your
        access token here>"`` string to ensure that
        :meth:`~xyzservices.TileProvider.requires_token` method works properly.

        Returns
        -------
        bool

        Examples
        --------
        >>> import xyzservices.providers as xyz
        >>> xyz.MapBox.requires_token()
        True

        >>> xyz.CartoDB.Positron
        False

        We can specify this API key by calling the object or overriding the attribute.
        Overriding the attribute will alter existing object:

        >>> xyz.OpenWeatherMap.Clouds["apiKey"] = "my-private-api-key"

        Calling the object will return a copy:

        >>> xyz.OpenWeatherMap.Clouds(apiKey="my-private-api-key")


        """
        # both attribute and placeholder in url are required to make it work
        for key, val in self.items():
            if isinstance(val, str) and "<insert your" in val:
                if key in self.url:
                    return True
        return False

    def _repr_html_(self, inside=False):
        provider_info = ""
        for key, val in self.items():
            if key != "name":
                provider_info += f"<dt><span>{key}</span></dt><dd>{val}</dd>"

        style = "" if inside else f"<style>{CSS_STYLE}</style>"
        html = f"""
        <div>
        {style}
            <div class="xyz-wrap">
                <div class="xyz-header">
                    <div class="xyz-obj">xyzservices.TileProvider</div>
                    <div class="xyz-name">{self.name}</div>
                </div>
                <div class="xyz-details">
                    <dl class="xyz-attrs">
                        {provider_info}
                    </dl>
                </div>
            </div>
        </div>
        """

        return html


def _load_json(f):

    data = json.loads(f)

    providers = Bunch()

    for provider_name in data.keys():
        provider = data[provider_name]

        if "url" in provider.keys():
            providers[provider_name] = TileProvider(provider)

        else:
            providers[provider_name] = Bunch(
                {i: TileProvider(provider[i]) for i in provider}
            )

    return providers


CSS_STYLE = """
/* CSS stylesheet for displaying xyzservices objects in Jupyter.*/
.xyz-header {
    padding-top: 6px;
    padding-bottom: 6px;
    margin-bottom: 4px;
    border-bottom: solid 1px #ddd;
}

.xyz-header>div {
    display: inline;
    margin-top: 0;
    margin-bottom: 0;
}

.xyz-obj,
.xyz-name {
    margin-left: 2px;
    margin-right: 10px;
}

.xyz-obj {
    color: #555;
}

.xyz-name {
    color: #000;
}

.xyz-attrs {
    grid-column: 1 / -1;
}

dl.xyz-attrs {
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: 125px auto;
    background-color: rgb(244, 244, 244);
}

.xyz-attrs dt,
dd {
    padding: 0;
    margin: 0;
    float: left;
    padding-right: 10px;
    width: auto;
}

.xyz-attrs dt {
    font-weight: normal;
    grid-column: 1;
}

.xyz-attrs dt:hover span {
    display: inline-block;
    background: #fff;
    padding-right: 10px;
}

.xyz-attrs dd {
    grid-column: 2;
    white-space: pre-wrap;
    word-break: break-all;
}

.xyz-details ul>li>label>span {
    color: #555;
    padding-left: 10px;
}

.xyz-inside {
    display: none;
}

.xyz-checkbox:checked~.xyz-inside {
    display: contents;
}

.xyz-collapsible li>input {
    display: none;
}

.xyz-collapsible>li>label {
    cursor: pointer;
}

.xyz-collapsible>li>label:hover {
    color: #555;
}

ul.xyz-collapsible {
    list-style: none!important;
    padding-left: 20px!important;
}

.xyz-checkbox+label:before {
    content: '►';
    font-size: 11px;
}

.xyz-checkbox:checked+label:before {
    content: '▼';
}

.xyz-wrap {
    margin-bottom: 10px;
}
"""
