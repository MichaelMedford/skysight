import os
import platform

print("System: {name} {system} {release}".format(name=os.name,
                                                 system=platform.system(),
                                                 release=platform.release()))

import sys

print("Python: " + sys.version)

import pytest

print("pytest: " + pytest.__version__)

import numpy

print("numpy: " + numpy.__version__)

import shapely

print("shapely: " + shapely.__version__)

import descartes

print("descartes imported")

import skysight

print("skysight: " + skysight.__version__)
