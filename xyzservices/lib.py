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


def _load_json(path):

    with open(path, "r") as f:
        data = json.load(f)

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
