#! /usr/bin/env python
#

""" Slew translations and/or rotations to be applied to a a single Camera
or to a list of Cameras. """

from itertools import combinations


class Slew:
    """
    Class for the geometric manipulation of Camera objects. Each Camera
    object is created from the *camera.Camera* class and can be either
    translated or rotated by a Slew.

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
        1) Applying a Slew to a single camera:
            slew = Slew(degrees = 10, raOffset = 0.1, decOffset = -0.2)
            camera = Camera(coordsList)
            slew.apply(camera)

        1) Applying a Slew to a list of cameras:
            slewList = []
            slewList.append(Slew(degrees = 10,
                                 raOffset = 0.1,
                                 decOffset = -0.2))
            slewList.append(Slew(degrees = 20,
                                 raOffset = -0.1,
                                 decOffset = 0.2))

            cameraList = []
            for slew in slewList:
                camera = Camera(coordsList)
                slew.apply(camera)
                cameraList.append(camera)
    """

    def __init__(self, degrees=0, raOffset=0, decOffset=0):
        self.degrees = degrees
        self.raOffset = raOffset
        self.decOffset = decOffset

    def apply(self, camera):
        """
        Applies the attributes of the Slew to the *camera*.

        Parameters:
            camera : *camera.Camera* object
                An object from the camera.Camera class containing a *poly*
                and a *coordsList*.
        """
        camera.rotate(degrees=self.degrees)
        camera.translate(raOffset=self.raOffset,
                         decOffset=self.decOffset)


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
        if intersectCam is None:  # Initiates the intersectCam variable
            intersectCam = camera
        else:
            intersectCam = intersectCam.intersect(camera)

    return intersectCam


def return_union(cameraList, excludeList=None):
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
        if unionCam is None:  # Initiates the unionCam variable
            unionCam = camera
        else:
            unionCam = unionCam.union(camera)

    # If not union has been found, return an empty Camera
    if unionCam is None:
        from skysight.camera import emptyCamera
        unionCam = emptyCamera

    return unionCam


def return_ditherDict(camera, slewList):
    """
    Returns a dictionary with the amount of area which is overlapping for
    each number of exposures in the dither.

    Parameters:
        camera : *camera.Camera*
            A camera which will be run through the slewList.
        slewList : *list* of *dither.Slew* objects
            A list of slews from the *dither.Slew* class, each to be
            applied to a copy of the *camera*.

    Returns:
        ditherDict : *dict*
            A dictionary containing the amount of area which is overlapping
            for each number of exposures in the dither. The keys of the
            dictionary will be the number of overlaps included in the area,
            and the values will be the amount of that overlap area in square
            degrees.
    """
    # The number of overlaps is equal to the number of slews.
    dims = len(slewList)

    # Create a list of cameras with each dither in the slewList applied
    cameraList = []
    for i in range(dims):
        cameraCopy = camera.copy()
        slewList[i].apply(cameraCopy)
        cameraList.append(cameraCopy)

    # For each number of possible exposures, calculate the amount of area
    # overlapping in the dither pattern
    ditherDict = {}
    for dim in range(1, dims + 1):
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
