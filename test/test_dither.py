import pytest

from skysight import camera
from skysight import dither
import numpy as np

def compare_coords(coord1, coord2):
	assert np.isclose(coord1[0], coord2[0], atol=1e-2)
	assert np.isclose(coord1[1], coord2[1], atol=1e-2)

def compare_coordsLists(coordsList1, coordsList2):
	assert len(coordsList1) == len(coordsList2)
	for coords1, coords2 in zip(coordsList1, coordsList2):
		assert len(coords1) == len(coords2)
		for coord1, coord2 in zip(coords1, coords2):
			compare_coords(coord1,coord2)

def test_slew():
	slew = dither.Slew()
	assert slew.raOffset == 0
	assert slew.decOffset == 0
	assert slew.degrees == 0

@pytest.fixture
def squareCoords():
	"""Returns a unit square camera with LL corner at the origin."""
	return [[(-1.0,-1.0),(-1.0,1.0),(1.0,1.0),(1.0,-1.0),(-1.0,-1.0)]]

@pytest.fixture
def squareCamera():
	"""Returns a unit square camera with LL corner at the origin."""
	return camera.Camera(squareCoords())

@pytest.mark.parametrize('raOffset, decOffset', [
	(0, 1),
	(1, 0),
	(0, -1),
	(-1, 0),
	(-1, 1),
	(0, -1),
])

def test_slew_translate(squareCamera, raOffset, decOffset):
	squareCameraSlew = squareCamera.copy()
	slew = dither.Slew(raOffset = raOffset, decOffset = decOffset)
	slew.apply(squareCameraSlew)
	print(squareCameraSlew.get_coordsList())

	squareCamera.translate(raOffset = raOffset, decOffset = decOffset)
	print(squareCamera.get_coordsList())

	compare_coordsLists(squareCamera.get_coordsList(),squareCameraSlew.get_coordsList())

@pytest.mark.parametrize('degrees', [
	(-60),
	(-30),
	(0),
	(30),
	(60)
])

def test_slew_rotate(squareCamera, degrees):
	squareCameraSlew = squareCamera.copy()
	slew = dither.Slew(degrees = degrees)
	slew.apply(squareCameraSlew)

	squareCamera.rotate(degrees = degrees)

	compare_coordsLists(squareCamera.get_coordsList(),squareCameraSlew.get_coordsList())

@pytest.mark.parametrize('raOffset, decOffset, degrees', [
	(.5, 1, 10),
	(1, .5, 10),
	(.5, -1, 45),
	(-1, .5, 45),
	(-1, 1, -120),
	(1, -1, -120),
])

def test_ditherDict_theoretical_2D(squareCamera, raOffset, decOffset, degrees):

	slewList = []
	slewList.append(dither.Slew(raOffset = raOffset, decOffset = decOffset, degrees = degrees))
	slewList.append(dither.Slew(raOffset = raOffset * 2, decOffset = decOffset * 2, degrees = degrees * 2))

	cameraA = squareCamera.copy()
	cameraB = squareCamera.copy()

	slewList[0].apply(cameraA)
	slewList[1].apply(cameraB)

	cameraAB = cameraA.intersect(cameraB)

	area1 = cameraA.difference(cameraB).get_area()
	area1 += cameraB.difference(cameraA).get_area()

	area2 = cameraAB.get_area()

	ditherDict = dither.return_ditherDict(squareCamera, slewList)

	assert np.isclose(ditherDict[1], area1, atol=1e-8)
	assert np.isclose(ditherDict[2], area2, atol=1e-8)

@pytest.mark.parametrize('raOffset, decOffset, degrees', [
	(0.5, 1, 10),
	(1, 0.5, 10),
	(0.5, -1, 45),
	(-1, 0.5, 45),
	(-1, 1, -120),
	(1, -1, -120),
])

def test_ditherDict_theoretical_3D(squareCamera, raOffset, decOffset, degrees):

	slewList = []
	slewList.append(dither.Slew(raOffset = raOffset, decOffset = decOffset, degrees = degrees))
	slewList.append(dither.Slew(raOffset = raOffset * 2, decOffset = decOffset * 2, degrees = degrees * 2))
	slewList.append(dither.Slew(raOffset = raOffset * 3, decOffset = decOffset * 3, degrees = degrees * 3))

	cameraA = squareCamera.copy()
	cameraB = squareCamera.copy()
	cameraC = squareCamera.copy()

	slewList[0].apply(cameraA)
	slewList[1].apply(cameraB)
	slewList[2].apply(cameraC)

	area1 = cameraA.difference(cameraB.union(cameraC)).get_area()
	area1 += cameraB.difference(cameraA.union(cameraC)).get_area()
	area1 += cameraC.difference(cameraA.union(cameraB)).get_area()

	area2 = cameraA.intersect(cameraB).difference(cameraC).get_area()
	area2 += cameraB.intersect(cameraC).difference(cameraA).get_area()

	area3 = cameraA.intersect(cameraB).intersect(cameraC).get_area()

	ditherDict = dither.return_ditherDict(squareCamera, slewList)

	assert np.isclose(ditherDict[1], area1, atol=1e-8)
	assert np.isclose(ditherDict[2], area2, atol=1e-8)
	assert np.isclose(ditherDict[3], area3, atol=1e-8)

@pytest.mark.parametrize('raOffset, decOffset, degrees, ditherDict', [
	(.05, .1, 10, {1:0.8322901532105128,
				 2:0.6602651340037049,
				 3:0.5516005915160114,
				 4:0.4785037140714401,
				 5:2.8554350071531296}),
	(.05, .2, 20, {1:1.4841493943462285,
				 2:0.9554865449606817,
				 3:0.8703295552430503,
				 4:0.8433894967720252,
				 5:2.123938248378486}),
	(-.1, .05, 20, {1:1.1398676701840769,
				 2:0.713262401254041,
				 3:0.5726654224379046,
				 4:0.5992275460790507,
				 5:0.5386764144347223,
				 6:2.437326736633181}),
])

def test_ditherDict_hardcoded(squareCamera, raOffset, decOffset, degrees, ditherDict):

	slewList = []
	for i in range(len(ditherDict)):
		slewList.append(dither.Slew(raOffset = raOffset*i, decOffset = decOffset*i, degrees = degrees*i))

	ditherDict_calc = dither.return_ditherDict(squareCamera, slewList)

	for i in range(1,len(ditherDict)+1):
		assert np.isclose(ditherDict[i], ditherDict_calc[i], atol=1e-8)
