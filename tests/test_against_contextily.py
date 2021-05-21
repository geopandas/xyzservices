"""
Temporary tests againts contextily providers to ensure the
functionality of xyzservices mirrors the existing one in contextily.

Will be replaced by the actual tests once the loading machinery is in place.
"""

from contextily import providers
import xyzservices as xyz

_all = providers.keys()


def test_all():
    for source in _all:
        assert providers[source] == getattr(xyz, source)
