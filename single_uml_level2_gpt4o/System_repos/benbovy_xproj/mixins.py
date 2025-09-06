# mixins.py

from typing import Hashable, Any
import xarray as xr
import pyproj

class ProjAccessorMixin:
    def _proj_set_crs(self, spatial_ref, crs):
        """
        Method called when setting a new CRS via
        :py:meth:`xarray.Dataset.proj.assign_crs()`.

        Parameters
        spatial_ref : Hashable
            The name of the spatial reference (scalar) coordinate
            to which the CRS has been set.
        crs : pyproj.crs.CRS
            The new CRS attached to the spatial reference coordinate.

        Returns
        xarray.Dataset or xarray.DataArray
            Either a new or an existing Dataset or DataArray.
        """
        raise NotImplementedError

class ProjIndexMixin:
    def _proj_get_crs(self):
        """
        XProj access to the CRS of the index.

        Returns
        pyproj.crs.CRS or None
            The CRS of the index or None if not (yet) defined.
        """
        raise NotImplementedError

    def _proj_set_crs(self, spatial_ref, crs):
        """
        Method called when mapping a CRS to index coordinate(s) via
        :py:meth:`xarray.Dataset.proj.map_crs`.

        Parameters
        spatial_ref : Hashable
            The name of the spatial reference (scalar) coordinate.
        crs : pyproj.crs.CRS
            The new CRS attached to the spatial reference coordinate.

        Returns
        Index
            Either a new or an existing xarray Index.
        """
        raise NotImplementedError

    def _proj_to_crs(self, spatial_ref, crs):
        """
        Method called when mapping a CRS to index coordinate(s) via
        :py:meth:`xarray.Dataset.proj.map_crs` with ``transform=True``.

        Parameters
        spatial_ref : Hashable
            The name of the spatial reference (scalar) coordinate.
        crs : pyproj.crs.CRS
            The new CRS attached to the spatial reference coordinate.

        Returns
        Index
            Either a new or an existing xarray Index.
        """
        raise NotImplementedError