#! /usr/bin/env python
#

""" Dither translations and/or rotations to be applied to a a single Camera
or to a list of Cameras. """

class Dither:
	"""
	Class for the manipulation of Camera objects through a Dither 
	translation or rotation. Each Camera object is created from the Camera 
	class in camera.py and can be either translated or rotated by a Dither.

	Attributes:
		degrees : *float*
			The number of degrees by which to rotate a Camera's CCDs.
		ra_offset : *float*
			The number of degrees by which to translate a Camera's CCDs in 
			right ascension.
		dec_offset : *float*
			The number of degrees by which to translate a Camera's CCDs in 
			declination.

	Examples:
		1) Applying a Dither to a single camera:
			dither = Dither(degrees = 10, ra_offset = 0.1, dec_offset = -0.2)
			camera = Camera(coords_list)
			dither.apply(camera)

		1) Applying a Dither to a list of cameras:
			dither_list = []
			dither_list.append(Dither(degrees = 10, ra_offset = 0.1, dec_offset = -0.2))
			dither_list.append(Dither(degrees = 20, ra_offset = -0.1, dec_offset = 0.2))
			
			camera_list = []
			for dither in dither_list:
				camera = Camera(coords_list)
				dither.apply(camera)
				camera_list.append(camera)
	"""

	def __init__(self, degrees = 0, ra_offset = 0, dec_offset = 0):
		self.degrees = degrees
		self.ra_offset = ra_offset
		self.dec_offset = dec_offset

	def apply(self, camera):
		"""
		Applies the attributes of the Dither to the *camera*.

		Parameters:
			camera : *camera.Camera object*
				An object from the camera.Camera class containing a *poly* 
				and a *coords_list*.
		"""
		camera.rotate(degrees = self.degrees)
		camera.translate(ra_offset = self.ra_offset,
					  dec_offset = self.dec_offset)
		