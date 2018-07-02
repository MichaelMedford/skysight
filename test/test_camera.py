import pytest

from skysight import camera
import numpy as np

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
	assert squareCamera.get_center() == (0.0, 0.0)

def test_squareCamera_centroid(squareCamera):
	assert squareCamera.get_centroid() == (0.0, 0.0)

def test_squareCamera_buffer(squareCamera):
	squareCamera.buffer(1.0, 128)
	assert np.isclose(squareCamera.get_area(), 15.141513801144306, atol=1e-10)

def test_squareCamera_buffer_undo(squareCamera):
	squareCamera.buffer(1.0, 128)
	squareCamera.buffer(-1.0, 128)
	assert np.isclose(squareCamera.get_area(), 4.0, atol=1e-6)

def compare_coordsLists(coordsList1, coordsList2):
	assert len(coordsList1) == len(coordsList2)
	for coords1, coords2 in zip(coordsList1, coordsList2):
		assert len(coords1) == len(coords2)
		for (coord1x, coord1y), (coord2x, coord2y) in zip(coords1, coords2):
			assert np.isclose(coord1x, coord2x, atol=1e-2)
			assert np.isclose(coord1y, coord2y, atol=1e-2)

# @pytest.mark.parametrize('raOffset, decOffset, coordsList', [
# 	(1, 0, [[(1.0,0.0),(1.0,1.0),(2.0,1.0),(2.0,0.0),(1.0,0.0)]]),
# 	(0, 1, [[(0.0,1.0),(0.0,2.0),(1.0,2.0),(1.0,1.0),(0.0,1.0)]]),
# 	(-1, 2, [[(-1.0,2.0),(-1.0,3.0),(0.0,3.0),(0.0,2.0),(-1.0,2.0)]])
# ])

# def test_squareCamera_translate(squareCamera, raOffset, decOffset, coordsList):
# 	squareCamera.translate(raOffset = raOffset, decOffset = decOffset)
# 	compare_coordsLists(squareCamera.get_coordsList(),coordsList)

# @pytest.mark.parametrize('degrees, coordsList', [
# 	(90, [[(1.0,0.0),(0.0,0.0),(0.0,1.0),(1.0,1.0),(1.0,0.0)]]),
# 	(-90, [[(0.0,1.0),(1.0,1.0),(1.0,0.0),(0.0,0.0),(0.0,1.0)]]),
# 	(45, [[(0,0),
# 		   (-np.cos(np.radians(45)),np.cos(np.radians(45))),
# 		   (0,2*np.cos(np.radians(45))),
# 		   (np.cos(np.radians(45)),np.cos(np.radians(45))),
# 		   (0,0)]]),
# 	(-45, [[(0,0),
# 		   (np.cos(np.radians(45)),np.cos(np.radians(45))),
# 		   (2*np.cos(np.radians(45)),0),
# 		   (np.cos(np.radians(45)),-np.cos(np.radians(45))),
# 		   (0,0)]])
# ])

# def test_squareCamera_rotate(squareCamera, degrees, coordsList):
# 	squareCamera.rotate(degrees = degrees)
# 	compare_coordsLists(squareCamera.get_coordsList(),coordsList)

# @pytest.mark.parametrize('degrees, coordsList', [
# 	(90, [[(0.0,0.0),(-1.0,0.0),(-1.0,1.0),(0.0,1.0),(0.0,0.0)]]),
# 	(-90, [[(0.0,0.0),(1.0,0.0),(1.0,-1.0),(0.0,-1.0),(0.0,0.0)]]),
# 	(45, [[(0,0),
# 		   (-np.cos(np.radians(45)),np.cos(np.radians(45))),
# 		   (0,2*np.cos(np.radians(45))),
# 		   (np.cos(np.radians(45)),np.cos(np.radians(45))),
# 		   (0,0)]]),
# 	(-45, [[(0,0),
# 		   (np.cos(np.radians(45)),np.cos(np.radians(45))),
# 		   (2*np.cos(np.radians(45)),0),
# 		   (np.cos(np.radians(45)),-np.cos(np.radians(45))),
# 		   (0,0)]])
# ])

# def test_squareCamera_rotate_origin(squareCamera, degrees, coordsList):
# 	squareCamera.rotate(degrees = degrees, origin = True)
# 	compare_coordsLists(squareCamera.get_coordsList(),coordsList)
