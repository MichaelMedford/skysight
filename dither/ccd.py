#! /usr/bin/env python
#

""" Loading, transforming and comparing the corners of Camera CCDs."""

import numpy as np
from shapely import geometry
from shapely import affinity
from shapely.ops import cascaded_union
from descartes import PolygonPatch

class Camera:

	"""
	Class for collection and manipulation of a camera's CCD corner
	coordinates. A list of CCD corner coordinates is inputted as a 
	*coords_list*, resulting in a shapely.geometry.multipolygon object 
	stored in *poly*. This *poly* can be geometrically translated and 
	rotated to model astronomical dither patterns.

	Attributes:
		coords_list : *list*
			List of coordinates of the corners of each CCD in the camera. 
			The *coords_list* must follow these rules:

			1) Coordinates are (ra, dec) numeric pairs of the angular 
			   position of each camera's corners. 
			2) The *coords_list* must contain at least one CCD. If there 
			   is only one CCD in the *coords_list*, then it must be passed 
			   to the Camera as a list of length 1.
			2) Each CCD in the *coords_list* must contain at least three 
			   corners.
			4) The CCDs in the *coords_list* CANNOT overlap.

			Example:
			1) For a *coord_list* of two CCDs:
				coords_list = [ [(0,0),(0,1),(1,1),(1,0)],
								[(2,2),(2,3),(3,3),(3,2)] ]
				ccd = Camera(coords_list)

			2) For a *coord_list* of one CCD:
				coords_list = [ [(0,0),(0,1),(1,1),(1,0)] ]
				ccd = Camera(coords_list)

		name : *str*, optional
			Name by which to identify a Camera.
	"""
	def __init__(self, coords_list, name=None):

		if not isinstance(coords_list[0], list):
			raise TypeError ('coords_list must be a list of coordinates '
							 'for the corners of each CCD in the camera.')

		if name is not None and not isinstance(name, str):
			raise TypeError ('Camera name must be a string.')

		# Combine corners of the CCDs in the coords_list into one poly
		polys = []
		for coords in coords_list:
			polys.append(geometry.Polygon(coords))
		self.poly = cascaded_union(polys)
		self.name = name

	@property
	def poly(self):
		return self._poly
	
	@poly.setter
	def poly(self, new_poly):
		"""
		Sets the new poly and updates the Camera's coords_list

		Parameters:
			new_poly : *shapely.geometry.multipolygon.MultiPolygon*
					   or
					   *shapely.geometry.multipolygon.Polygon*
				Sets the polygon for this Camera as *new_poly*, as well 
				as updating the *coords_list*.
		"""
		self._poly = new_poly
		self.coords_list = self.get_coords_list()

	def get_coords_list(self):
		"""
		Returns the *corods_list* for THIS Camera's *poly*. This list will 
		follow the conventions for a *coords_list* as outlined in the 
		Camera Attributes.
		"""
		return self._get_coords_list(self.poly)

	def _get_coords_list(self, poly):
		"""
		Returns the *corods_list* for ANY Camera's *poly*. This list will 
		follow the conventions for a *coords_list* as outlined in the 
		Camera Attributes.

		Parameters:
			poly : *shapely.geometry.multipolygon.MultiPolygon*
				   or
				   *shapely.geometry.multipolygon.Polygon*
				Polygon from which a *coords_list* will be calculated.
		"""
		if poly.area == 0:
			# If Camera is an empty polygon
			coords_list = [[(0,0),(0,0),(0,0)]]

		elif poly.type == 'MultiPolygon':
			# If Cameara is a collection of multiple polygons
			coords_list = []
			for p in poly:
				coords = []
				for x,y in p.exterior.coords:
					coords.append((x,y))
				coords_list.append(coords)

		elif poly.type == 'Polygon':
			# If Camera is a single polygon
			coords = []
			for x,y in poly.exterior.coords:
				coords.append((x,y))
			coords_list = [coords]

		return coords_list

	def copy(self):
		"""
		Returns a copy of the current Camera.
		"""
		return Camera(self.coords_list)

	def buffer(self, buffer):
		"""
		Expands the coundaries of each polygon in the Camera's *poly* 
		by the size of the *buffer*.
		Parameters:
			buffer : *float*
				The number of degrees by which each polygon in *poly* 
				will be expanded.
		"""
		self.poly = self.poly.buffer(buffer)

	def expand_ra(self):
		"""
		Applys a spherical distortion to the Camera's coordinates to 
		adjust for the declination of the Camera's current position.
		This function must be called AFTER geometric transformations 
		(translate, rotate) have been applied.
		"""
		centroid = self.get_center()
		polys = []
		for coords in self.coords_list:
			new_coords = []
			for (coord_x,coord_y) in coords:
				coord_x -= centroid[0]
				coord_x /= np.cos(np.radians(coord_y))
				coord_x += centroid[0]
				new_coords.append((coord_x,coord_y))
			polys.append(geometry.Polygon(new_coords))
		self.poly = cascaded_union(polys)

	def collapse_ra(self):
		"""
		Applys a spherical distortion to the Camera's coordinates to 
		adjust for the declination of the Camera's current position. 
		This function must be called BEFORE geometric transformations 
		(translate, rotate) have been applied.
		"""
		centroid = self.get_center()
		polys = []
		for coords in self.coords_list:
			new_coords = []
			for (coord_x,coord_y) in coords:
				coord_x -= centroid[0]
				coord_x *= np.cos(np.radians(coord_y))
				coord_x += centroid[0]
				new_coords.append((coord_x,coord_y))
			polys.append(geometry.Polygon(new_coords))
		self.poly = cascaded_union(polys)

	def rotate(self, degrees=0):
		"""
		Rotates the Camera's *poly* by *degrees*. This is a rotation around 
		the origin (0,0), not around each polygon's center. Prior to and 
		after rotation, *poly* is adjusted to account for spherical 
		distrotion effects at different declinations.

		Parameters:
			degrees : *float*
				The number of degrees by which to rotate *poly*.
		"""
		self.collapse_ra()
		self.poly = affinity.rotate(self.poly, degrees)
		self.expand_ra()

	def translate(self, ra_offset=0, dec_offset=0):
		"""
		Translates the Camera's *poly* by *ra_offset* and *dec_offset*. 
		Prior to and after rotation, the Camera's *poly* is adjusted 
		to account for spherical  distrotion effects at different 
		declinations.

		Parameters:
			ra_offset : *float*
				The number of degrees by which to translate *poly* in 
				right ascension.
			dec_offset : *float*
				The number of degrees by which to translate *poly* in 
				declination.
		"""
		self.collapse_ra()
		self.poly = affinity.translate(self.poly,
									   xoff=ra_offset,
									   yoff=dec_offset)
		self.expand_ra()

	def get_radius(self):
		"""
		Returns the radius of the smallest circle which could encompass 
		all of the polygons in the Camera's *poly*. If the Camera's *poly* 
		is centered around (0,0), the radius is equal to the distance to 
		the polygon corner furthest from the Camera's center. Radius is 
		returned in degrees.
		"""
		center = self.get_center()
		radius_list = []
		for coords in self.coords_list:
			for coord in coords:
				radius = np.sqrt((coord[0]-center[0])**2. + (coord[1]-center[1])**2.)
				radius_list.append(radius)
		return np.max(radius_list)

	def get_area(self):
		"""
		Returns the total area of all polygons in the Camera's *poly*. 
		Area is returned in square degrees.
		"""
		return self.poly.area

	def get_limits(self):
		"""
		Returns the coordinates of the smallest box which could surround 
		all of the polygons in the Camera's *poly*. Limits are returned 
		in degrees.

		Returns:
			ra_lim, dec_lim : *tuple* of *floats*
				Two tuples, each containing the range of the Camera's *poly* 
				in right ascension and declination respectively.
		"""
		if self.poly.type == 'Polygon':
			# If Camera is a single polygon
			x_arr = []
			y_arr = []
			for x,y in self.poly.exterior.coords:
				x_arr.append(x)
				y_arr.append(y)
		else:
			# If Camera is a collection of multiple polygons
			x_arr = []
			y_arr = []
			for poly in self.poly:
				for x,y in poly.exterior.coords:
					x_arr.append(x)
					y_arr.append(y)

		ra_lim = (min(x_arr),max(x_arr))
		dec_lim = (min(y_arr),max(y_arr))

		return ra_lim, dec_lim

	def get_center(self, ra_offset=0, dec_offset=0):
		"""
		Returns the geometric center of the smallest box which could 
		surround all of the polygons in the Camera's *poly*. The center 
		is returned in degrees. User can apply a forced offset to the 
		right ascension or declination of the center if there is a known 
		asymmetry in the Camera's design.

		Parameters:
			ra_offset : *float*
				The number of degrees by which to offset the *poly* center 
				in right ascension.
			dec_offset : *float*
				The number of degrees by which to offset the *poly* center 
				in declination.

		Returns:
			center_ra, center_dec : *float*
				Two floats at the center location of the Camera's *poly*.
		"""
		bounds = self.poly.bounds
		center_ra = np.mean([bounds[0],bounds[2]]) + ra_offset
		center_dec = np.mean([bounds[1],bounds[3]]) + dec_offset
		return center_ra, center_dec

	def get_centroid(self, ra_offset=0, dec_offset=0):
		"""
		Returns the geometric centroid of the Camera's *poly*, as 
		calculated by the Shapely package. The centroid is returned in 
		degrees. User can apply a forced offset to the right ascension or 
		declination to the centroid if there is a known asymmetry in the 
		Camera's design.

		Parameters:
			ra_offset : *float*
				The number of degrees by which to offset the *poly* 
				centroid in right ascension.
			dec_offset : *float*
				The number of degrees by which to offset the *poly* 
				centroid in declination.

		Returns:
			centroid_ra, centroid_dec : *float*
				Two floats at the centroid location of the Camera's *poly*.
		"""
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

		centroid_ra = np.mean(centroid_x_list) + ra_offset
		centroid_dec = np.mean(centroid_x_list) + dec_offset
		return centroid_ra, centroid_dec

	def intersect(self, camera):
		"""
		Calculates the intersection between this Camera's *poly* and the 
		*poly* of the *camera* passed as a parameter. The intersection is 
		then returned as a Camera object.

		Parameters:
			camera : *ccd.Camera object*
				An object from the ccd.Camera class containing a *poly* 
				and a "*coords_list".

		Returns:
			camera : *ccd.Camera object*
				An object from the ccd.Camera class that is the 
				intersection between this Camera and the *camera* 
				parameter.
		"""
		intersect_poly = self.poly.intersection(camera.poly)
		coords_list = self._get_coords_list(intersect_poly)
		return Camera(coords_list)

	def union(self, camera):
		"""
		Calculates the union between this Camera's *poly* and the 
		*poly* of the *camera* passed as a parameter. The union is 
		then returned as a Camera object.

		Parameters:
			camera : *ccd.Camera object*
				An object from the ccd.Camera class containing a *poly* 
				and a "*coords_list".

		Returns:
			camera : *ccd.Camera object*
				An object from the ccd.Camera class that is the 
				union between this Camera and the *camera* 
				parameter.
		"""
		union_poly = cascaded_union([self.poly,camera.poly])
		coords_list = self._get_coords_list(union_poly)
		return Camera(coords_list)

	def difference(self, camera):
		"""
		Calculates the difference between this Camera's *poly* and the 
		*poly* of the *camera* passed as a parameter. The difference is 
		then returned as a Camera object.

		Parameters:
			camera : *ccd.Camera object*
				An object from the ccd.Camera class containing a *poly* 
				and a "*coords_list".

		Returns:
			camera : *ccd.Camera object*
				An object from the ccd.Camera class that is the 
				difference between this Camera and the *camera* 
				parameter.
		"""
		difference_poly = self.poly.difference(camera.poly)
		coords_list = self._get_coords_list(difference_poly)
		return Camera(coords_list)

	def plot(self, ax, color='k', alpha=0.5, xlim=None, ylim=None):
		"""
		Plots the Camera's *poly* onto an axis object from Matplotlib. 
		The user can specify the color and transparency of *poly*. Unless 
		the xlim and ylim of the Matplotlib axis is specified by the user, 
		this command will set the limits of the axis to surround just the 
		Camera's *poly*.

		Parameters:
			ax : *matplotlib.axes._subplots.AxesSubplot*
				A Matplotlib axes object from the plt.subplots() command.
			color : *str*
				A color string compatible with a Matplotlib axis specifying 
				the color of the *poly*.
			alpha : *float*
				A number between 0 and 1 specifying the transparency of 
				the *poly*
			xlim : *tuple* of *floats*
				The range of x values with which to plot the *poly*
			ylim : *tuple* of *floats*
				The range of y values with which to plot the *poly*

		Example:
			1) For a single Camera object
				ccd = Camera(coords_list)
				fig,ax = plt.subplots()
				ccd.plot(ax, color='g', alpha=0.3)

			2) For multiple Camera objects
				ccd = Camera(coords_list)
				ccd2 = Camera(coords_list)
				ccd2.translate(ra_offset=1.0)
				fig,ax = plt.subplots()
				ccd.plot(ax, color='g', alpha=0.3, xlim=(-2,2), ylim=(-2,2))
				ccd2.plot(ax, color='b', alpha=0.3, xlim=(-2,2), ylim=(-2,2))
		"""
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
	"""
	Returns the CCD coordinates of the MACHO camera as a ccd.Camera 
	object.
	"""
	from dither import corners
	corners = corners.load_macho_corners()
	ccd = Camera([corners], name='macho')
	return ccd

def return_hsc_ccd():
	"""
	Returns the CCD coordinates of the Hyper-Supreme Camera as a 
	ccd.Camera object.
	"""
	from dither import corners
	corners = corners.load_hsc_corners()
	ccd = Camera(corners, name='hsc')
	return ccd

def return_decam_ccd():
	"""
	Returns the CCD coordinates of the Dark Energy Camera as a 
	ccd.Camera object.
	"""
	from dither import corners
	corners = corners.load_decam_corners()
	ccd = Camera(corners, name='decam')
	return ccd
