import pytest

from skysight import camera
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

def test_camera_import():
	cam = camera.return_decamCamera()
	cam = camera.return_decamCamera()
	cam = camera.return_hscCamera()

@pytest.fixture
def emptyCoords():
	"""Returns a unit square camera with LL corner at the origin."""
	return [[(0.0,0.0),(0.0,0.0),(0.0,0.0)]]

@pytest.fixture
def emptyCamera():
	"""Returns a unit square camera with LL corner at the origin."""
	return camera.Camera(emptyCoords())

def test_emptyCamera_file(emptyCamera):
	assert emptyCamera.get_coordsList() == camera.emptyCamera.get_coordsList()

def test_emptyCamera_coords(emptyCamera):
	assert emptyCamera.get_coordsList() == emptyCoords()

def test_emptyCamera_coords_hidden(emptyCamera):
	assert emptyCamera._get_coordsList(emptyCamera.poly) == emptyCoords()

def test_emptyCamera_copy(emptyCamera):
	emptyCameraCopy = emptyCamera.copy()
	assert emptyCamera.get_coordsList() == emptyCameraCopy.get_coordsList()

def test_emptyCamera_area(emptyCamera):
	assert emptyCamera.get_area() == 0.0

def test_emptyCamera_radius(emptyCamera):
	assert emptyCamera.get_radius() == 0.0

def test_emptyCamera_limits(emptyCamera):
	assert emptyCamera.get_limits() == ((0.0, 0.0), (0.0, 0.0))

def test_emptyCamera_center(emptyCamera):
	assert emptyCamera.get_center() == (0.0, 0.0)

def test_emptyCamera_centroid(emptyCamera):
	assert emptyCamera.get_centroid() == (0.0, 0.0)

def test_emptyCamera_buffer(emptyCamera):
	emptyCamera.buffer(1.0, 128)
	assert np.isclose(emptyCamera.get_area(), np.pi, atol=1e-4)

@pytest.fixture
def squareCoords():
	"""Returns a unit square camera with LL corner at the origin."""
	return [[(-1.0,-1.0),(-1.0,1.0),(1.0,1.0),(1.0,-1.0),(-1.0,-1.0)]]

@pytest.fixture
def squareCamera():
	"""Returns a unit square camera with LL corner at the origin."""
	return camera.Camera(squareCoords())

def test_squareCamera_coords(squareCamera):
	assert squareCamera.get_coordsList() == squareCoords()

def test_squareCamera_coords_hidden(squareCamera):
	assert squareCamera._get_coordsList(squareCamera.poly) == squareCoords()

def test_squareCamera_copy(squareCamera):
	squareCameraCopy = squareCamera.copy()
	assert squareCamera.get_coordsList() == squareCameraCopy.get_coordsList()

@pytest.mark.parametrize('raOffset, decOffset, degrees', [
	(0, 1, 10),
	(1, 0, 10),
	(0, -1, 45),
	(-1, 0, 45),
	(-1, 1, -120),
	(0, -1, -120)
])

def test_squareCamera_area(squareCamera, raOffset, decOffset, degrees):
	assert squareCamera.get_area() == 4.0
	squareCamera.translate(raOffset = raOffset, decOffset = decOffset)
	assert np.isclose(squareCamera.get_area(), 4.0, atol=1e-2)
	squareCamera.rotate(degrees = degrees)
	assert np.isclose(squareCamera.get_area(), 4.0, atol=1e-2)
	squareCamera.rotate(degrees = degrees, origin = True)
	assert np.isclose(squareCamera.get_area(), 4.0, atol=1e-2)

@pytest.mark.parametrize('raOffset, decOffset, degrees', [
	(0, 1, 10),
	(1, 0, 10),
	(0, -1, 45),
	(-1, 0, 45),
	(-1, 1, -120),
	(0, -1, -120)
])

def test_squareCamera_radius(squareCamera, raOffset, decOffset, degrees):
	assert np.isclose(squareCamera.get_radius(), np.sqrt(2), atol=1e-3)
	squareCamera.translate(raOffset = raOffset, decOffset = decOffset)
	assert np.isclose(squareCamera.get_radius(), np.sqrt(2), atol=1e-3)
	squareCamera.rotate(degrees = degrees)
	assert np.isclose(squareCamera.get_radius(), np.sqrt(2), atol=1e-3)
	squareCamera.rotate(degrees = degrees, origin = True)
	assert np.isclose(squareCamera.get_radius(), np.sqrt(2), atol=1e-3)

def test_squareCamera_limits(squareCamera):
	assert squareCamera.get_limits() == ((-1.0, 1.0), (-1.0, 1.0))

def test_squareCamera_center(squareCamera):
	compare_coords(squareCamera.get_center(),(0.0, 0.0))
	squareCamera.translate(raOffset = 20)
	compare_coords(squareCamera.get_center(),(20.0, 0.0))
	squareCamera.translate(decOffset = 40)
	compare_coords(squareCamera.get_center(),(20.0, 40.0))

def test_squareCamera_centroid(squareCamera):
	compare_coords(squareCamera.get_centroid(),(0.0, 0.0))
	squareCamera.translate(raOffset = 20)
	compare_coords(squareCamera.get_centroid(),(20.0, 0.0))
	squareCamera.translate(decOffset = 40)
	compare_coords(squareCamera.get_centroid(),(20.0, 40.0))

def test_squareCamera_buffer(squareCamera):
	squareCamera.buffer(1.0, 128)
	assert np.isclose(squareCamera.get_area(), 15.141513801144306, atol=1e-10)

def test_squareCamera_buffer_undo(squareCamera):
	squareCamera.buffer(1.0, 128)
	squareCamera.buffer(-1.0, 128)
	assert np.isclose(squareCamera.get_area(), 4.0, atol=1e-6)

@pytest.mark.parametrize('raOffset, decOffset, coordsList', [
	(1, 0, [[(0.0,-1.0),(0.0,1.0),(2.0,1.0),(2.0,-1.0),(0.0,-1.0)]]),
	(0, 1, [[(-1.0,0),(-1.0,2.0),(1.0,2.0),(1.0,0),(-1.0,0.0)]]),
	(-1, 2, [[(-2.0,1.0),(-2.0,3.0),(0.0,3.0),(0.0,1.0),(-2.0,1.0)]])
])

def test_squareCamera_translate(squareCamera, raOffset, decOffset, coordsList):
	squareCamera.translate(raOffset = raOffset, decOffset = decOffset)
	compare_coordsLists(squareCamera.get_coordsList(),coordsList)

@pytest.mark.parametrize('degrees, coordsList', [
	(90, [[(1.0,-1.0),(-1.0,-1.0),(-1.0,1.0),(1.0,1.0),(1.0,-1.0)]]),
	(-90, [[(-1.0,1.0),(1.0,1.0),(1.0,-1.0),(-1.0,-1.0),(-1.0,1.0)]]),
	(45, [[(0,-np.sqrt(2)),
		    (-np.sqrt(2),0),
		    (0.0,np.sqrt(2)),
		    (np.sqrt(2),0),
		    (0.0,-np.sqrt(2))]]),
	(-45, [[(-np.sqrt(2),0.0),
		    (0.0,np.sqrt(2)),
		    (np.sqrt(2),0.0),
		    (0.0,-np.sqrt(2)),
		    (-np.sqrt(2),0.0)]])
])

def test_squareCamera_rotate(squareCamera, degrees, coordsList):
	squareCamera.rotate(degrees = degrees)
	compare_coordsLists(squareCamera.get_coordsList(),coordsList)

@pytest.mark.parametrize('raOffset, decOffset', [
	(0, 0),
	(60, 0),
	(-60, 0),
	(0, -60),
	(60, -60),
	(-60, -60),
	(0, 60),
	(60, 60),
	(-60, 60)
])

def test_squareCamera_ra_expand_collapse(squareCoords, squareCamera, raOffset, decOffset):
	coordsList = []
	for coord in squareCoords[0]:
		dec = decOffset + coord[1]
		ra = raOffset + (coord[0] / np.cos(np.radians(dec)))
		coordsList.append((ra, dec))
	coordsList = [coordsList]

	squareCamera.translate(raOffset=raOffset, decOffset=decOffset)

	compare_coordsLists(squareCamera.get_coordsList(),coordsList)

@pytest.mark.parametrize('raOffset, decOffset, area', [
	(0.5, 0, 3.0),
	(-0.5, 0, 3.0),
	(0, 0.5, 3.0),
	(0, -0.5, 3.0),
	(-0.5, 0.5, 2.25),
	(0.5, -0.5, 2.25)
])

def test_squareCamera_intersect(squareCamera, raOffset, decOffset, area):

	squareCamera2 = squareCamera.copy()
	squareCamera2.translate(raOffset = raOffset, decOffset = decOffset)
	intersect = squareCamera.intersect(squareCamera2)
	assert np.isclose(intersect.get_area(), area, atol=1e-2)

@pytest.mark.parametrize('raOffset, decOffset, area', [
	(0.5, 0, 5.0),
	(-0.5, 0, 5.0),
	(0, 0.5, 5.0),
	(0, -0.5, 5.0),
	(-0.5, 0.5, 5.75),
	(0.5, -0.5, 5.75)
])

def test_squareCamera_union(squareCamera, raOffset, decOffset, area):

	squareCamera2 = squareCamera.copy()
	squareCamera2.translate(raOffset = raOffset, decOffset = decOffset)
	union = squareCamera.union(squareCamera2)
	assert np.isclose(union.get_area(), area, atol=1e-2)

@pytest.mark.parametrize('raOffset, decOffset, area', [
	(0.5, 0, 1.0),
	(-0.5, 0, 1.0),
	(0, 0.5, 1.0),
	(0, -0.5, 1.0),
	(-0.5, 0.5, 1.75),
	(0.5, -0.5, 1.75)
])

def test_squareCamera_difference(squareCamera, raOffset, decOffset, area):

	squareCamera2 = squareCamera.copy()
	squareCamera2.translate(raOffset = raOffset, decOffset = decOffset)
	assert np.isclose(squareCamera.difference(squareCamera2).get_area(), area, atol=1e-2)
	assert np.isclose(squareCamera2.difference(squareCamera).get_area(), area, atol=1e-2)

@pytest.mark.parametrize('raOffset, decOffset, area', [
	(0.5,0,2.0),
	(-0.5,0,2.0),
	(0,0.5,2.0),
	(0,-0.5,2.0),
	(-0.5,0.5,1.0),
	(0.5,-0.5,1.0),
])

def test_squareCamera_intersect_three(squareCamera, raOffset, decOffset, area):
	squareCamera2 = squareCamera.copy()
	squareCamera2.translate(raOffset = raOffset, decOffset = decOffset)
	squareCamera3 = squareCamera.copy()
	squareCamera3.translate(raOffset = raOffset * 2, decOffset = decOffset * 2)
	assert np.isclose(squareCamera.intersect(squareCamera2).intersect(squareCamera3).get_area(), area, atol=1e-2)

@pytest.mark.parametrize('raOffset, decOffset, area', [
	(0.5,0,6.0),
	(-0.5,0,6.0),
	(0,0.5,6.0),
	(0,-0.5,6.0),
	(-0.5,0.5,7.5),
	(0.5,-0.5,7.5),
])

def test_squareCamera_union_three(squareCamera, raOffset, decOffset, area):
	squareCamera2 = squareCamera.copy()
	squareCamera2.translate(raOffset = raOffset, decOffset = decOffset)
	squareCamera3 = squareCamera.copy()
	squareCamera3.translate(raOffset = raOffset * 2, decOffset = decOffset * 2)
	assert np.isclose(squareCamera.union(squareCamera2).union(squareCamera3).get_area(), area, atol=1e-2)

@pytest.mark.parametrize('raOffset, decOffset, area1, area2', [
	(0.25,0,0.5,0),
	(-0.25,0,0.5,0),
	(0,0.5,1.0,0),
	(0,-0.5,1.0,0),
	(-0.25,0.5,.25*2+(2*.5)-(.5*.25),0.25),
	(0.25,-0.5,.25*2+(2*.5)-(.5*.25),0.25),
])

def test_squareCamera_difference_three(squareCamera, raOffset, decOffset, area1, area2):
	squareCamera2 = squareCamera.copy()
	squareCamera2.translate(raOffset = raOffset, decOffset = decOffset)
	squareCamera3 = squareCamera.copy()
	squareCamera3.translate(raOffset = raOffset * 2, decOffset = decOffset * 2)
	assert np.isclose(squareCamera.difference(squareCamera2).difference(squareCamera3).get_area(), area1, atol=1e-2)
	assert np.isclose(squareCamera.difference(squareCamera3).difference(squareCamera2).get_area(), area1, atol=1e-2)
	assert np.isclose(squareCamera2.difference(squareCamera3).difference(squareCamera).get_area(), area2, atol=1e-2)
	assert np.isclose(squareCamera2.difference(squareCamera).difference(squareCamera3).get_area(), area2, atol=1e-2)
	assert np.isclose(squareCamera3.difference(squareCamera).difference(squareCamera2).get_area(), area1, atol=1e-2)
	assert np.isclose(squareCamera3.difference(squareCamera2).difference(squareCamera).get_area(), area1, atol=1e-2)
