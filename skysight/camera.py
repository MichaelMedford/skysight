#! /usr/bin/env python
#

""" Loading, transforming and comparing the corners of Camera CCDs."""

import numpy as np
from shapely import geometry
from shapely import affinity
from shapely.ops import cascaded_union
from descartes import PolygonPatch

##############################
#                            #
#  Camera Class              #
#                            #
##############################

class Camera:
	"""
	Class for collection and manipulation of a camera's CCD corner
	coordinates. A list of CCD corner coordinates is inputted as a 
	*coordsList*, resulting in a shapely.geometry.multipolygon object 
	stored in *poly*. This *poly* can be geometrically translated and 
	rotated to model astronomical dither patterns.

	Attributes:
		coordsList : *list*
			List of coordinates of the corners of each CCD in the camera. 
			The *coordsList* must follow these rules:

			1) Coordinates are (ra, dec) numeric pairs of the angular 
			   position of each camera's corners. 
			2) The *coordsList* must contain at least one CCD. If there 
			   is only one CCD in the *coordsList*, then it must be passed 
			   to the Camera as a list of length 1.
			2) Each CCD in the *coordsList* must contain at least three 
			   corners.
			4) The CCDs in the *coordsList* CANNOT overlap.
		name : *str*, optional
			Name by which to identify a Camera.

	Examples:
		1) For a *coordsList* of two CCDs:
			coordsList = [ [(0,0),(0,1),(1,1),(1,0)],
						[(2,2),(2,3),(3,3),(3,2)] ]
			camera = Camera(coordsList)

		2) For a *coordsList* of one CCD.
			coordsList = [ [(0,0),(0,1),(1,1),(1,0)] ]
			camera = Camera(coordsList)
	"""
	def __init__(self, coordsList, name = None):

		if not isinstance(coordsList[0], list):
			raise TypeError ('coordsList must be a list of coordinates '
							 'for the corners of each CCD in the camera.')

		if name is not None and not isinstance(name, str):
			raise TypeError ('Camera name must be a string.')

		# Combine corners of the CCDs in the coordsList into one poly
		polys = []
		for coords in coordsList:
			polys.append(geometry.Polygon(coords))
		self.poly = cascaded_union(polys)
		self.name = name

	@property
	def poly(self):
		return self.Poly
	
	@poly.setter
	def poly(self, newPoly):
		"""
		Sets the new poly and updates the Camera's coordsList

		Parameters:
			newPoly : *shapely.geometry.multipolygon.MultiPolygon*
					   or
					   *shapely.geometry.multipolygon.Polygon*
				Sets the polygon for this Camera as *newPoly*, as well 
				as updating the *coordsList*.
		"""
		self.Poly = newPoly
		self.coordsList = self.get_coordsList()

	def get_coordsList(self):
		"""
		Returns the *coordsList* for THIS Camera's *poly*. This list will 
		follow the conventions for a *coordsList* as outlined in the 
		Camera Attributes.
		"""
		return self._get_coordsList(self.poly)

	def _get_coordsList(self, poly):
		"""
		Returns the *coordsList* for ANY Camera's *poly*. This list will 
		follow the conventions for a *coordsList* as outlined in the 
		Camera Attributes.

		Parameters:
			poly : *shapely.geometry.multipolygon.MultiPolygon*
				   or
				   *shapely.geometry.multipolygon.Polygon*
				Polygon from which a *coordsList* will be calculated.
		"""
		if poly.area == 0:
			# If Camera is an empty polygon
			coordsList = [[(0,0),(0,0),(0,0)]]

		elif poly.type == 'MultiPolygon':
			# If Cameara is a collection of multiple polygons
			coordsList = []
			for p in poly:
				coords = []
				for x,y in p.exterior.coords:
					coords.append((x,y))
				coordsList.append(coords)

		elif poly.type == 'Polygon':
			# If Camera is a single polygon
			coords = []
			for x,y in poly.exterior.coords:
				coords.append((x,y))
			coordsList = [coords]

		return coordsList

	def copy(self):
		"""
		Returns a copy of the current Camera.
		"""
		return Camera(self.coordsList)

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
		for coords in self.coordsList:
			new_coords = []
			for (coordX,coordY) in coords:
				coordX -= centroid[0]
				coordX /= np.cos(np.radians(coordY))
				coordX += centroid[0]
				new_coords.append((coordX,coordY))
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
		for coords in self.coordsList:
			new_coords = []
			for (coordX,coordY) in coords:
				coordX -= centroid[0]
				coordX *= np.cos(np.radians(coordY))
				coordX += centroid[0]
				new_coords.append((coordX,coordY))
			polys.append(geometry.Polygon(new_coords))
		self.poly = cascaded_union(polys)

	def rotate(self, degrees = 0, origin = False):
		"""
		Rotates the Camera's *poly* by *degrees*. This is a rotation 
		around each polygon's center, not the origin (0,0). Rotation 
		can be performed around the origin by setting the *origin* flag to 
		True. Prior to and after rotation, *poly* is adjusted to account 
		for spherical distrotion effects at different declinations.

		Parameters:
			degrees : *float*
				The number of degrees by which to rotate *poly*. Positive 
				angles are counter-clockwise and negative are clockwise 
				rotations.
			origin : *bool*
				Rotates the Camera's *poly* around the center of the *poly* 
				bounding box. If set to False, rotation will be performed 
				around the origin.
		"""
		self.collapse_ra()
		if not origin:
			self.poly = affinity.rotate(self.poly, degrees)
		else:
			self.poly = affinity.rotate(self.poly, degrees, origin = (0,0))
		self.expand_ra()

	def translate(self, raOffset = 0, decOffset = 0):
		"""
		Translates the Camera's *poly* by *raOffset* and *decOffset*. 
		Prior to and after rotation, the Camera's *poly* is adjusted 
		to account for spherical  distrotion effects at different 
		declinations.

		Parameters:
			raOffset : *float*
				The number of degrees by which to translate *poly* in 
				right ascension.
			decOffset : *float*
				The number of degrees by which to translate *poly* in 
				declination.
		"""
		self.collapse_ra()
		self.poly = affinity.translate(self.poly,
									   xoff = raOffset,
									   yoff = decOffset)
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
		for coords in self.coordsList:
			for coord in coords:
				radius = np.sqrt( (coord[0] - center[0])**2. + 
								  (coord[1] - center[1])**2. )
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
			xArr = []
			yArr = []
			for x,y in self.poly.exterior.coords:
				xArr.append(x)
				yArr.append(y)
		else:
			# If Camera is a collection of multiple polygons
			xArr = []
			yArr = []
			for poly in self.poly:
				for x,y in poly.exterior.coords:
					xArr.append(x)
					yArr.append(y)

		ra_lim = (min(xArr),max(xArr))
		dec_lim = (min(yArr),max(yArr))

		return ra_lim, dec_lim

	def get_center(self, raOffset = 0, decOffset = 0):
		"""
		Returns the geometric center of the smallest box which could 
		surround all of the polygons in the Camera's *poly*. The center 
		is returned in degrees. User can apply a forced offset to the 
		right ascension or declination of the center if there is a known 
		asymmetry in the Camera's design.

		Parameters:
			raOffset : *float*
				The number of degrees by which to offset the *poly* center 
				in right ascension.
			decOffset : *float*
				The number of degrees by which to offset the *poly* center 
				in declination.

		Returns:
			centerRa, centerDec : *float*
				Two floats at the center location of the Camera's *poly*.
		"""
		bounds = self.poly.bounds
		centerRa = np.mean([bounds[0], bounds[2]]) + raOffset
		centerDec = np.mean([bounds[1], bounds[3]]) + decOffset
		return centerRa, centerDec

	def get_centroid(self, raOffset = 0, decOffset = 0):
		"""
		Returns the geometric centroid of the Camera's *poly*, as 
		calculated by the Shapely package. The centroid is returned in 
		degrees. User can apply a forced offset to the right ascension or 
		declination to the centroid if there is a known asymmetry in the 
		Camera's design.

		Parameters:
			raOffset : *float*
				The number of degrees by which to offset the *poly* 
				centroid in right ascension.
			decOffset : *float*
				The number of degrees by which to offset the *poly* 
				centroid in declination.

		Returns:
			centroidRa, centroidDec : *float*
				Two floats at the centroid location of the Camera's *poly*.
		"""
		if self.poly.type == 'Polygon':
			for x,y in self.poly.centroid.coords:
				return (x,y)
		else:
			centroidXList = []
			centroidYList = []
			for poly in self.poly:
				for x,y in self.poly.centroid.coords:
					centroidXList.append(x)
					centroidYList.append(y)

		centroidRa = np.mean(centroidXList) + raOffset
		centroidDec = np.mean(centroidYList) + decOffset
		return centroidRa, centroidDec

	def intersect(self, camera):
		"""
		Calculates the intersection between this Camera's *poly* and the 
		*poly* of the *camera* passed as a parameter. The intersection is 
		then returned as a Camera object.

		Parameters:
			camera : *camera.Camera* object
				An object from the camera.Camera class containing a *poly* 
				and a *coordsList*.

		Returns:
			camera : *camera.Camera* object
				An object from the camera.Camera class that is the 
				intersection between this Camera and the *camera* 
				parameter.
		"""
		intersectPoly = self.poly.intersection(camera.poly)
		coordsList = self._get_coordsList(intersectPoly)
		return Camera(coordsList)

	def union(self, camera):
		"""
		Calculates the union between this Camera's *poly* and the 
		*poly* of the *camera* passed as a parameter. The union is 
		then returned as a Camera object.

		Parameters:
			camera : *camera.Camera* object
				An object from the camera.Camera class containing a *poly* 
				and a *coordsList*.

		Returns:
			camera : *camera.Camera* object
				An object from the camera.Camera class that is the 
				union between this Camera and the *camera* 
				parameter.
		"""
		unionPoly = cascaded_union([self.poly,camera.poly])
		coordsList = self._get_coordsList(unionPoly)
		return Camera(coordsList)

	def difference(self, camera):
		"""
		Calculates the difference between this Camera's *poly* and the 
		*poly* of the *camera* passed as a parameter. The difference is 
		then returned as a Camera object.

		Parameters:
			camera : *camera.Camera* object
				An object from the camera.Camera class containing a *poly* 
				and a *coordsList*.

		Returns:
			camera : *camera.Camera* object
				An object from the camera.Camera class that is the 
				difference between this Camera and the *camera* 
				parameter.
		"""
		differencePoly = self.poly.difference(camera.poly)
		coordsList = self._get_coordsList(differencePoly)
		return Camera(coordsList)

	def plot(self, ax,
				   color = 'k',
				   alpha = 0.5,
				   xlim = None,
				   ylim = None):
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
				camera = Camera(coordsList)
				fig,ax = plt.subplots()
				camera.plot(ax, color='g', alpha=0.3)

			2) For multiple Camera objects
				camera = Camera(coordsList)
				camera2 = Camera(coordsList)
				camera2.translate(raOffset=1.0)
				fig,ax = plt.subplots()
				camera.plot(ax, color='g', alpha=0.3, xlim=(-2,2), ylim=(-2,2))
				camera2.plot(ax, color='b', alpha=0.3, xlim=(-2,2), ylim=(-2,2))
		"""
		ax.add_patch(PolygonPatch(self.poly,
								  fc = color,
								  alpha = alpha))

		if xlim == None or ylim == None:
			xlimPoly, ylimPoly = self.get_limits()

		if xlim == None:
			ax.set_xlim(xlimPoly)
		else:
			ax.set_xlim(xlim)

		if ylim == None:
			ax.set_ylim(ylimPoly)
		else:
			ax.set_ylim(ylim)

emptyCamera = Camera([[(0,0),(0,0),(0,0)]])

##############################
#                            #
#  Return Known Cameras      #
#                            #
##############################

def return_machoCamera():
	"""
	Returns the CCD coordinates of the MACHO camera as a camera.Camera 
	object.
	"""
	from skysight import corners
	corners = corners.load_machoCorners()
	machoCamera = Camera([corners], name = 'macho')
	return machoCamera

def return_hscCamera():
	"""
	Returns the CCD coordinates of the Hyper-Supreme Camera as a 
	camera.Camera object.
	"""
	from skysight import corners
	corners = corners.load_hscCorners()
	hscCamera = Camera(corners, name = 'hsc')
	return hscCamera

def return_decamCamera():
	"""
	Returns the CCD coordinates of the Dark Energy Camera as a 
	camera.Camera object.
	"""
	from skysight import corners
	corners = corners.load_decamCorners()
	decamCamera = Camera(corners, name = 'decam')
	return decamCamera
