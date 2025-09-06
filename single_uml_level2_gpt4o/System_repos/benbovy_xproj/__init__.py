# __init__.py

__version__ = "0.1.0"
__all__ = ["ProjAccessor", "CRSIndex", "CRSProxy", "GeoAccessorRegistry", "ProjAccessorMixin", "ProjIndexMixin", "Frozen", "FrozenDict", "register_accessor", "either_dict_or_kwargs", "is_crs_aware", "format_compact_cf", "format_full_cf_gdal"]

from .accessor import ProjAccessor, register_accessor, either_dict_or_kwargs, is_crs_aware
from .index import CRSIndex
from .crs_utils import format_compact_cf, format_full_cf_gdal
from .mixins import ProjAccessorMixin, ProjIndexMixin
from .utils import Frozen, FrozenDict
from .accessor import GeoAccessorRegistry

# noqa: F401