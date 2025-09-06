import xarray as xr
import pyproj
from typing import Any, Mapping, Hashable
from .index import CRSIndex
from .utils import Frozen, FrozenDict

T_AccessorClass = Any

def register_accessor(accessor_cls):
    """Decorator for registering a geospatial, CRS-dependent Xarray
    (Dataset and/or DataArray) accessor.

    Parameters
    
    accessor_cls : class
        A Python class that has been decorated with
        :py:func:`xarray.register_dataset_accessor` and/or
        :py:func:`xarray.register_dataarray_accessor`.
        It is important that this decorator is applied on top of
        those Xarray decorators.
    """
    # Implementation here
    pass

def either_dict_or_kwargs(positional, keyword, func_name):
    """Resolve combination of positional and keyword arguments.

    Based on xarray's ``either_dict_or_kwargs``.
    """
    # Implementation here
    pass

def is_crs_aware(index):
    """Determine whether a given xarray Index is CRS-aware by checking if it is an instance of ProjIndexMixin or has the method "_proj_get_crs"."""
    # Implementation here
    pass

class ProjAccessor:
    """Xarray `.proj` extension entry-point."""

    def __init__(self, obj):
        self.obj = obj
        self._cache_all_crs_indexes()

    def __call__(self, coord_name):
        """Select a given CRS by coordinate name.

        Parameter
        
        coord_name : Hashable
            Either the name of a (scalar) spatial reference coordinate with a
            :py:class:`~xproj.CRSIndex` or the name of a coordinate with an
            index that implements XProj's CRS interface.

        Returns
        
        proxy
            A proxy accessor for a single CRS.
        """
        # Implementation here
        pass

    def _cache_all_crs_indexes(self):
        """Cache all CRSIndex objects and CRS-aware Index objects from the object's xindexes into separate dictionaries for quick access."""
        # Implementation here
        pass

    def _get_crs_index(self, coord_name):
        """Retrieve the CRSIndex associated with a specified coordinate name in a Dataset or DataArray, ensuring the coordinate exists, is scalar, and has a valid CRSIndex."""
        # Implementation here
        pass

    def _update_crs_info(self, spatial_ref, func):
        """Update the Coordinate Reference System (CRS) information in an xarray object by applying a given function to specified spatial reference coordinates or all CRS indexes if none are specified."""
        # Implementation here
        pass

    def assert_one_crs_index(self):
        """Raise an `AssertionError` if no or multiple CRS-indexed coordinates
        are found in the Dataset or DataArray."""
        # Implementation here
        pass

    def assign_crs(self, spatial_ref_crs, allow_override=False, **spatial_ref_crs_kwargs):
        """Assign one or more spatial reference coordinate variables, each with
        a given coordinate reference system (CRS).

        Doesn't trigger any coordinate transformation or data resampling.

        Parameters
        
        spatial_ref_crs : dict-like or None, optional
            A dict where the keys are the names of the (scalar) coordinate variables
            and values target CRS in any format accepted by
            :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>` such
            as an authority string (e.g. ``"EPSG:4326"``), EPSG code (e.g. ``4326``) or
            a WKT string.
            If the coordinate(s) doesn't exist it will be created.
        allow_override : bool, default False
            Allow to replace the index if the coordinates already have an index.
        **spatial_ref_crs_kwargs : optional
            The keyword arguments form of ``spatial_ref_crs``.
            One of ``spatial_ref_crs`` or ``spatial_ref_crs_kwargs`` must be provided.

        Returns
        
        Dataset or DataArray
            A new Dataset or DataArray object with new or updated
            :term:`spatial reference coordinate` variables.
        """
        # Implementation here
        pass

    def clear_crs_info(self, spatial_ref=None):
        """Convenient method to clear all attributes of one or all spatial
        reference coordinates.

        Parameters
        
        spatial_ref : Hashable, optional
            The name of a :term:`spatial reference coordinate`. If not provided (default),
            CRS information will be cleared for all spatial reference coordinates found in
            the Dataset or DataArray. Each spatial reference coordinate must already have
            a :py:class:`~xproj.CRSIndex` associated.

        Returns
        
        Dataset or DataArray
            A new Dataset or DatArray object with attributes cleared for one or all
            spatial reference coordinates.

        See Also
        
        Dataset.proj.write_crs_info
        DataArray.proj.write_crs_info
        """
        # Implementation here
        pass

    @property
    def crs(self):
        """Return the coordinate reference system as a :py:class:`pyproj.crs.CRS`
        object, or ``None`` if there isn't any.

        Raises an error if multiple CRS are found in the Dataset or DataArray."""
        # Implementation here
        pass

    @property
    def crs_aware_indexes(self):
        """Return an immutable dictionary of coordinate names as keys and
        xarray Index objects that are CRS-aware.

        A :term:`CRS-aware index` is an :py:class:`xarray.Index` object that
        must at least implements a method like
        :py:meth:`~xproj.ProjIndexMixin._proj_get_crs`."""
        # Implementation here
        pass

    @property
    def crs_indexes(self):
        """Return an immutable dictionary of coordinate names as keys and
        :py:class:`~xproj.CRSIndex` objects as values.

        Return an empty dictionary if no coordinate with a CRSIndex is found."""
        # Implementation here
        pass

    def map_crs(self, spatial_ref_coords, allow_override=False, transform=False, **spatial_ref_coords_kwargs):
        """Map spatial reference coordinate(s) to other indexed coordinates.

        This has an effect only if the latter coordinates have a
        :term:`CRS-aware index`. The index must then support setting the CRS via
        the :term:`proj index interface`.

        Parameters
        
        spatial_ref_coords : dict, optional
            A dict where the keys are the names of (scalar) spatial reference
            coordinates and values are the names of other coordinates with an index.
        allow_override : bool, optional
            If True, replace the CRS of the target index(es) even if they already have
            a CRS defined (default: False).
        transform : bool, optional
            If True (default: False), transform coordinate data to conform to the new CRS.
        **spatial_ref_coords_kwargs : optional
            The keyword arguments form of ``spatial_ref_coords``.
            One of ``spatial_ref_coords`` or ``spatial_ref_coords_kwargs`` must be provided.

        Returns
        
        Dataset or DataArray
            A new Dataset or DatArray object with updated CRS-aware indexes (and possibly
            updated coordinate data).
        """
        # Implementation here
        pass

    def write_crs_info(self, spatial_ref=None, func=None):
        """Write CRS information as attributes to one or all spatial
        reference coordinates.

        Parameters
        
        spatial_ref : Hashable, optional
            The name of a :term:`spatial reference coordinate`. If not provided (default),
            CRS information will be written to all spatial reference coordinates found in
            the Dataset or DataArray. Each spatial reference coordinate must already have
            a :py:class:`~xproj.CRSIndex` associated.
        func : callable, optional
            Any callable used to format CRS information as coordinate variable attributes.
            The default function adds a ``crs_wkt`` attribute for compatibility with
            CF conventions.

        Returns
        
        Dataset or DataArray
            A new Dataset or DatArray object with attributes updated for one or all
            spatial reference coordinates.

        See Also
        
        ~xproj.format_compact_cf
        ~xproj.format_full_cf_gdal
        Dataset.proj.clear_crs_info
        DataArray.proj.clear_crs_info
        """
        # Implementation here
        pass

class CRSProxy:
    """A proxy for a CRS(-aware) indexed coordinate."""

    def __init__(self, obj, coord_name, crs):
        self.obj = obj
        self.coord_name = coord_name
        self.crs = crs

    @property
    def crs(self):
        """Return the coordinate reference system as a :class:`pyproj.CRS` object."""
        # Implementation here
        pass

class GeoAccessorRegistry:
    """A registry of 3rd-party geospatial Xarray accessors."""

    _accessor_names = {}

    @classmethod
    def get_accessors(cls, xr_obj):
        """Retrieve a list of valid accessor objects from an xarray Dataset or DataArray based on predefined accessor names, excluding any that are instances of xr.DataArray."""
        # Implementation here
        pass

    @classmethod
    def register_accessor(cls, accessor_cls):
        """Register an Xarray Dataset or DataArray accessor class to a target class by updating the accessor names mapping for the respective Xarray classes."""
        # Implementation here
        pass