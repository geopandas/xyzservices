"""
Utilities to support XYZservices
"""
import json


class Bunch(dict):
    """A dict with attribute-access"""

    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __dir__(self):
        return self.keys()


class TileProvider(Bunch):
    """
    A dict with attribute-access and that
    can be called to update keys
    """

    def __call__(self, **kwargs):
        new = TileProvider(self)  # takes a copy preserving the class
        new.update(kwargs)
        return new

    def build_url(self, x=None, y=None, z=None, token=None, scale_factor=None):
        """
        Build the URL of tiles from the TileProvider object

        Can return URL with placeholders or the final tile URL.

        Attributes
        ----------

        x, y, z : int
            tile number
        token : str (optional)
            Access token (or API key or similar) for the tiles requiring one.
        scale_factor : str (optional)
            Scale factor (where supported). For example, you can get double resolution
            (512 x 512) instead of standard one (256 x 256) with ``"@2x"``. If you want
            to keep a placeholder, pass `"{r}"`.

        Returns
        -------

        url : str

        Examples
        --------
        >>> import xyzservices.providers as xyz

        >>> xyz.CartoDB.DarkMatter.build_url()
        'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'

        >>> xyz.CartoDB.DarkMatter.build_url(x=9, y=11, z=5)
        'https://a.basemaps.cartocdn.com/dark_all/5/9/11.png'

        >>> xyz.CartoDB.DarkMatter.build_url(x=9, y=11, z=5, scale_factor="@2x")
        'https://a.basemaps.cartocdn.com/dark_all/5/9/11@2x.png'

        >>> xyz.MapBox.build_url(token="my_token")
        'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=my_token'

        """
        provider = self.copy()

        if not x:
            x = "{x}"
        if not y:
            y = "{y}"
        if not z:
            z = "{z}"

        if token:
            for key, val in provider.items():
                if isinstance(val, str) and "<insert your" in val:
                    provider[key] = token

        url = provider.pop("url")
        subdomains = provider.pop("subdomains", "abc")
        if scale_factor:
            r = scale_factor
            provider.pop("r", None)
        else:
            r = provider.pop("r", "")

        return url.format(x=x, y=y, z=z, s=subdomains[0], r=r, **provider)


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
