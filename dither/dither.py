#! /usr/bin/env python
#

""" Dither translations and/or rotations to be applied to a a single Camera
or to a list of Cameras. """

from itertools import combinations

class Dither:
	"""
	Class for the manipulation of Camera objects through a Dither 
	translation or rotation. Each Camera object is created from the Camera 
	class in camera.py and can be either translated or rotated by a Dither.

	Attributes:
		degrees : *float*
			The number of degrees by which to rotate a Camera's CCDs.
		raOffset : *float*
			The number of degrees by which to translate a Camera's CCDs in 
			right ascension.
		decOffset : *float*
			The number of degrees by which to translate a Camera's CCDs in 
			declination.

	Examples:
		1) Applying a Dither to a single camera:
			dither = Dither(degrees = 10, raOffset = 0.1, decOffset = -0.2)
			camera = Camera(coords_list)
			dither.apply(camera)

		1) Applying a Dither to a list of cameras:
			dither_list = []
			dither_list.append(Dither(degrees = 10, raOffset = 0.1, decOffset = -0.2))
			dither_list.append(Dither(degrees = 20, raOffset = -0.1, decOffset = 0.2))
			
			camera_list = []
			for dither in dither_list:
				camera = Camera(coords_list)
				dither.apply(camera)
				camera_list.append(camera)
	"""

	def __init__(self, degrees = 0, raOffset = 0, decOffset = 0):
		self.degrees = degrees
		self.raOffset = raOffset
		self.decOffset = decOffset

	def apply(self, camera):
		"""
		Applies the attributes of the Dither to the *camera*.

		Parameters:
			camera : *camera.Camera object*
				An object from the camera.Camera class containing a *poly* 
				and a *coords_list*.
		"""
		camera.rotate(degrees = self.degrees)
		camera.translate(raOffset = self.raOffset,
					     decOffset = self.decOffset)

def return_intersect(cameraList):
	"""
	Calculates the intersection of the Camera objects in the *camera_list*.
	Function returns None if there exists no intersection.

	Parameters:
		cameraList : *camera.Camera object*
			An object from the camera.Camera class containing a *poly* 
			and a *coords_list*.

	Returns:
		camera : *camera.Camera object*
			An object from the camera.Camera class that is the 
			difference between this Camera and the *camera* 
			parameter.
	"""

	intersect = None
	for camera in camera_list:
		if intersect == None:
			intersect = c
		else:
			intersect = intersect.intersect(camera)

	if intersect == None:
		from dither.camera import Camera
		intersect = Camera([[(0,0),(0,0),(0,0)]])

	return intersect

def return_union(camera_list, exclude_camera_list):

	union = None
	for camera in camera_list:
		if camera in exclude_camera_list:
			continue
		if union == None:
			union = camera
		else:
			union = union.union(c)

	if union == None:
		from dither.camera import Camera
		union = Camera([[(0,0),(0,0),(0,0)]])

	return union

def return_exposure_area(coords_list, action_list):

	dims = len(action_list)

	CCD_list = []
	for i in range(dims):
		ccd = utils.CCDclass(coords_list)
		action_list[i].apply(ccd)
		CCD_list.append(ccd)

	area_arr = []
	for dim in range(1,dims+1):
		area_dim = 0
		for comb in combinations(CCD_list,dim):
			area_dim += (return_intersect(comb).difference(return_union(CCD_list,comb))).get_area()
		area_arr.append((dim,area_dim))

	return area_arr
