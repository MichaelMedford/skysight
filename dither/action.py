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
			camera = Camera(coordsList)
			dither.apply(camera)

		1) Applying a Dither to a list of cameras:
			dither_list = []
			dither_list.append(Dither(degrees = 10, raOffset = 0.1, decOffset = -0.2))
			dither_list.append(Dither(degrees = 20, raOffset = -0.1, decOffset = 0.2))
			
			camera_list = []
			for dither in dither_list:
				camera = Camera(coordsList)
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
			camera : *camera.Camera* object
				An object from the camera.Camera class containing a *poly* 
				and a *coordsList*.
		"""
		camera.rotate(degrees = self.degrees)
		camera.translate(raOffset = self.raOffset,
					     decOffset = self.decOffset)

def return_intersect(cameraList):
	"""
	Calculates the intersection of the Camera objects in the *cameraList*.
	Function returns an empty Camera if there exists no intersection.

	Parameters:
		cameraList : *list* of *camera.Camera* objects
			A list of cameras from the camera.Camera class, each containing 
			a *poly* and a *coordsList*.

	Returns:
		intersectCam : *camera.Camera* object
			An object from the camera.Camera class that is the 
			intersection between all cameras in the cameraList. If there 
			exists no interesction between any cameras in the camerList, 
			an empty Camera will be returned.
	"""
	intersectCam = None
	for camera in cameraList:
		if intersectCam == None: # Initiates the intersectCam variable
			intersectCam = camera
		else:
			intersectCam = intersectCam.intersect(camera)

	return intersectCam

def return_union(cameraList, excludeList = None):
	"""
	Calculates the union of the Camera objects in the *cameraList*. 
	An excludeList can be provided which can be skipped over. 
	The function returns an empty Camera if there exists no union, which 
	can only occur when all cameras in the cameraList are included in the 
	excludeList.

	Parameters:
		cameraList : *list* of *camera.Camera* objects
			A list of cameras from the camera.Camera class, each containing 
			a *poly* and a *coordsList*.
		excludeList : *list* of *camera.Camera* objects
			A list of cameras from the camera.Camera class, each containing 
			a *poly* and a *coordsList*. These cameras will not be included 
			in the calculated camera union.

	Returns:
		intersect : *camera.Camera* object
			An object from the camera.Camera class that is the 
			union between all cameras in the cameraList, excluding the 
			cameras in the excludeList.
	"""
	unionCam = None
	for camera in cameraList:
		if excludeList is not None and camera in excludeList:
			# Skip the camera if it is in the excludeList
			continue
		if unionCam == None: # Initiates the unionCam variable
			unionCam = camera
		else:
			unionCam = unionCam.union(camera)

	# If not union has been found, return an empty Camera
	if unionCam == None:
		from dither.camera import emptyCamera
		unionCam = emptyCamera

	return unionCam

def return_ditherDict(camera, ditherList):
	"""
	Returns a dictionary with the amount of area which is overlapping for 
	each number of exposures in the dither.

	Parameters:
		camera : *camera.Camera*
			A camera which will be run through the ditherList.
		ditherList : *list* of *camera.Camera* objects
			A list of cameras from the camera.Camera class, each containing 
			a *poly* and a *coordsList*. These cameras will not be included 
			in the calculated camera union.

	Returns:
		ditherDict : *dict*
			A dictionary containing the amount of area which is overlapping 
			for each number of exposures in the dither. The keys of the 
			dictionary will be the number of overlaps included in the area, 
			and the values will be the amount of that overlap area in square 
			degrees.
	"""
	# The number of overlaps is equal to the number of dithers.
	dims = len(ditherList)

	# Create a list of cameras with each dither in the ditherList applied
	cameraList = []
	for i in range(dims):
		cameraCopy = camera.copy()
		ditherList[i].apply(cameraCopy)
		cameraList.append(cameraCopy)

	# For each number of possible exposures, calculate the number of dithers
	ditherDict = {}
	for dim in range(1,dims+1):
		areaDim = 0
		for combinationList in combinations(cameraList, dim):
			# Intersection of all cameras in the combinationList
			intersectCam = return_intersect(combinationList)
			# Union of all cameras in the cameraList less the combinationList 
			unionCam = return_union(cameraList, combinationList)
			# Difference between the intersection and the union
			differenceCam = intersectCam.difference(unionCam)
			# Add the area of this difference to the total
			areaDim += differenceCam.get_area()
			
		ditherDict[dim] = areaDim

	return ditherDict
