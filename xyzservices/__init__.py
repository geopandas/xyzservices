from ._version import get_versions
from .lib import Bunch, TileProvider  # noqa
from .providers import providers  # noqa

__version__ = get_versions()["version"]
del get_versions
