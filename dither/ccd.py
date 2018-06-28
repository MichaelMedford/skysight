#! /usr/bin/env python
#

""" Loading and containing corners of CCDs. """

import numpy as np
from shapely import geometry
from shapely import affinity
from shapely.ops import cascaded_union
from descartes import PolygonPatch

class Camera():

	"""
	Class for collection and manipulation of camera's CCD corner
	coordinates.

	Attributes :
		coords_list: *list*
			List of coordinates for the corners of each CCD in the camera.
			Coordinates are (x, y) numeric pairs
			Each CCD must contain at least three corners.
			The coords_list must contain at least one CCD.

			Example:
				coords_list = [ [(0,0),(0,1),(1,1),(1,0)],
								[(2,2),(2,3),(3,3),(3,2)] ]
	"""

	def __init__(self, coords_list, name=None):

		if not isinstance(coords_list[0], list):
			raise TypeError ('coords_list must be a list of coordinates '
							 'for the corners of each CCD in the camera.')

		CCDS = []
		for coords in coords_list:
			CCDS.append(geometry.Polygon(coords))
		self.set_poly(cascaded_union(CCDS))
		self.name=name

	def set_poly(self, poly):
		self.poly = poly
		self.coords_list = self.get_coords_list()

	def get_coords_list(self):
		return self._get_coords_list(self.poly)

	def _get_coords_list(self, poly):
		if poly.area == 0:
			coords_list = [[(0,0),(0,0),(0,0)]]
		elif poly.type == 'MultiPolygon':
			coords_list = []
			for p in poly:
				coords = []
				for x,y in p.exterior.coords:
					coords.append((x,y))
				coords_list.append(coords)
		elif poly.type == 'Polygon':
			coords = []
			for x,y in poly.exterior.coords:
				coords.append((x,y))
			coords_list = [coords]
		else:
			print(poly.type)

		return coords_list

	def copy(self):
		if self.poly.type == 'Polygon':
			coords = []
			for x,y in self.poly.exterior.coords:
				coords.append((x,y))
			coords_list = [coords]
		else:
			coords_list = []
			for poly in self.poly:
				coords = []
				for x,y in poly.exterior.coords:
					coords.append((x,y))
				coords_list.append(coords)
		return CCD(coords_list)

	def buffer(self, buffer):
		self.set_poly(self.poly.buffer(buffer))

	def expand_ra(self):
		centroid = self.get_center()
		CCDS = []
		for coords in self.coords_list:
			new_coords = []
			for (coord_x,coord_y) in coords:
				coord_x -= centroid[0]
				coord_x /= np.cos(np.radians(coord_y))
				coord_x += centroid[0]
				new_coords.append((coord_x,coord_y))
			CCDS.append(geometry.Polygon(new_coords))
		self.set_poly(cascaded_union(CCDS))

	def collapse_ra(self):
		centroid = self.get_center()
		CCDS = []
		for coords in self.coords_list:
			new_coords = []
			for (coord_x,coord_y) in coords:
				coord_x -= centroid[0]
				coord_x *= np.cos(np.radians(coord_y))
				coord_x += centroid[0]
				new_coords.append((coord_x,coord_y))
			CCDS.append(geometry.Polygon(new_coords))
		self.set_poly(cascaded_union(CCDS))

	def rotate(self, degrees=0):
		self.collapse_ra()
		self.set_poly(affinity.rotate(self.poly, degrees))
		self.expand_ra()

	def translate(self, xoff=0, yoff=0):
		self.collapse_ra()
		self.set_poly(affinity.translate(self.poly, xoff, yoff))
		self.expand_ra()

	def get_radius(self):
		radius_list = []
		for coords in self.coords_list:
			for coord in coords:
				radius = np.sqrt(coord[0]**2. + coord[1]**2.)
				radius_list.append(radius)
		return np.max(radius_list)

	def get_area(self):
		return self.poly.area

	def get_limits(self):

		if self.poly.type == 'Polygon':
			x_arr = []
			y_arr = []
			for x,y in self.poly.exterior.coords:
				x_arr.append(x)
				y_arr.append(y)
		else:
			x_arr = []
			y_arr = []
			for poly in self.poly:
				for x,y in poly.exterior.coords:
					x_arr.append(x)
					y_arr.append(y)
		return (min(x_arr),max(x_arr)),(min(y_arr),max(y_arr))

	def get_center(self):
		bounds = self.poly.bounds
		x = np.mean([bounds[0],bounds[2]])
		y = np.mean([bounds[1],bounds[3]])
		y -= 33.95/3600.
		return (x,y)

	def get_centroid(self):

		if self.poly.type == 'Polygon':
			for x,y in self.poly.centroid.coords:
				return (x,y)
		else:
			centroid_x_list = []
			centroid_y_list = []
			for poly in self.poly:
				for x,y in self.poly.centroid.coords:
					centroid_x_list.append(x)
					centroid_y_list.append(y)
		return (np.mean(centroid_x_list),np.mean(centroid_y_list))

	def intersect(self, CCD):
		CCD_intersect_poly = self.poly.intersection(CCD.poly)
		coords_list = self._get_coords_list(CCD_intersect_poly)
		return CCD(coords_list)

	def union(self, CCD):
		CCD_union_poly = cascaded_union([self.poly,CCD.poly])
		coords_list = self._get_coords_list(CCD_union_poly)
		return CCD(coords_list)

	def difference(self, CCD):
		CCD_difference_poly = self.poly.difference(CCD.poly)
		coords_list = self._get_coords_list(CCD_difference_poly)
		return CCD(coords_list)

	def plot(self, ax, color='k', alpha=0.5, xlim=None, ylim=None):

		ax.add_patch(PolygonPatch(self.poly, fc=color, alpha=alpha))

		if xlim == None or ylim == None:
			xlim_poly,ylim_poly = self.get_limits()

		if xlim == None:
			ax.set_xlim(xlim_poly)
		else:
			ax.set_xlim(xlim)

		if ylim == None:
			ax.set_ylim(ylim_poly)
		else:
			ax.set_ylim(ylim)

def return_macho_ccd():

	from dither import corners
	corners = corners.load_macho_corners()
	ccd = CCD([corners], name='macho')
	return ccd

def return_hsc_ccd():

	from dither import corners
	corners = corners.load_hsc_corners()
	ccd = CCD([corners], name='hsc')
	return ccd

def return_decam_ccd():

	from dither import corners
	corners = corners.load_decam_corners()
	ccd = CCD([corners], name='decam')
	return ccd
