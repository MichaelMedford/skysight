#! /usr/bin/env python
#

""" Load Camera CCD corners of various telescope cameras. """

import os

data_dir = os.path.dirname(os.path.realpath(__file__))+"/data"

def load_macho_corners():
	"""
	Returns the CCD corners of the MACHO camera.

	Returns:
		corners : *list* of *float*
			A list of the angular degree offsets of the CCD corners.
	"""
	with open('%s/MACHO_corners.dat' % data_dir) as f:
		corners = eval(''.join(f.readlines()))[0]
	return corners

def load_decam_corners():
	"""
	Returns the CCD corners of the DECam camera.

	Returns:
		corners : *list* of *float*
			A list of the angular degree offsets of the CCD corners.
	"""
	with open('%s/DECam_corners.dat' % data_dir) as f:
		corners_dct = eval(''.join(f.readlines()))
		corners = [v for v in corners_dct.values()]
	return corners

def load_hsc_corners():
	"""
	Returns the CCD corners of the Hyper-Supreme Camera.

	Returns:
		corners : *list* of *float*
			A list of the angular degree offsets of the CCD corners.
	"""
	with open('%s/HSC_corners.dat' % data_dir) as f:
		corners_dct = eval(''.join(f.readlines()))
		corners = [v for v in corners_dct.values()]
	return corners
