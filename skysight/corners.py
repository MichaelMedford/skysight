#! /usr/bin/env python
#

""" Load Camera CCD corners of various telescope cameras. """

import os

data_dir = os.path.dirname(os.path.realpath(__file__)) + "/data"


def load_machoCorners():
    """
    Returns the CCD corners of the MACHO camera.

    Returns:
        machoCorners : *list* of *float*
            A list of the angular degree offsets of the CCD corners.
    """
    with open('%s/MACHO_corners.dat' % data_dir) as f:
        machoCorners = eval(''.join(f.readlines()))[0]
    return machoCorners


def load_decamCorners():
    """
    Returns the CCD corners of the DECam camera.

    Returns:
        decamCorners : *list* of *float*
            A list of the angular degree offsets of the CCD corners.
    """
    with open('%s/DECam_corners.dat' % data_dir) as f:
        corners_dct = eval(''.join(f.readlines()))
        decamCorners = [v for v in corners_dct.values()]
    return decamCorners


def load_hscCorners():
    """
    Returns the CCD corners of the Hyper-Supreme Camera.

    Returns:
        hscCorners : *list* of *float*
            A list of the angular degree offsets of the CCD corners.
    """
    with open('%s/HSC_corners.dat' % data_dir) as f:
        corners_dct = eval(''.join(f.readlines()))
        hscCorners = [v for v in corners_dct.values()]
    return hscCorners
