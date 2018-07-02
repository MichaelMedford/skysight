import pytest

from skysight import corners
import numpy as np

def test_machoCorners():
	machoCorners = corners.load_machoCorners()
	assert np.all(np.isclose(np.abs(machoCorners), 129/360., atol=1e-5))

def load_decamCorners():
	decamCorners = corners.load_decamCorners()
	assert len(decamCorners) == 60
	assert np.isclose(np.average(decamCorners), 0.0022692952057497885, atol=1e-10)

def load_hscCorners():
	hscCorners = corners.load_hscCorners()
	assert len(hscCorners) == 112
	assert np.isclose(np.average(hscCorners), 0.00047757257023303928, atol=1e-10)
