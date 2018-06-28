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

def action_

def action_CCDlist(CCDlist, action, name_arr):

	if type(name_arr[0]) in [int,np.int64]:
		name_arr = [str(n) for n in name_arr]

	for c in CCDlist:
		if c.name in name_arr:
			action.apply(c)

def remove_CCDlist(CCDlist, name_arr):

	if type(name_arr[0]) in [int,np.int64]:
		name_arr = [str(n) for n in name_arr]

	for c in CCDlist:
		if c.name in name_arr:
			CCDlist.remove(c)

def copy_CCDlist(CCDlist, name_arr):

	if type(name_arr[0]) in [int,np.int64]:
		name_arr = [str(n) for n in name_arr]

	new_list = []
	for name in name_arr:
		hsc_ccd = [c for c in CCDlist if c.name==name][0].copy()
		hsc_ccd.name = str(int(CCDlist[-1].name)+1)
		new_list.append(hsc_ccd.name)
		CCDlist.append(hsc_ccd)
	return CCDlist, new_list
