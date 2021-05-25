from .providers import providers
from .lib import Bunch, TileProvider

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
