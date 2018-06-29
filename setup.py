#! /usr/bin/env python
#

DESCRIPTION = 'A package for determining the optimal astronomical dither strategy'
DISTNAME = 'skysight'
AUTHOR = 'Michael Medford'
MAINTAINER = 'Michael Medford' 
MAINTAINER_EMAIL = 'MichaelMedford@berkeley.edu'
URL = 'https://github.com/MichaelMedford/skysight'
LICENSE = 'MIT License'
import skysight
VERSION = skysight.__version__

from setuptools import setup

if __name__ == "__main__":
        
    setup(name=DISTNAME,
          author=AUTHOR,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=open('README.md').read(),
          license=LICENSE,
          url=URL,
          version=VERSION,
          install_requires=['numpy','matplotlib','astropy','shapely','descartes'],
          packages=['skysight'],
          package_data={'skysight': ['data/*']},
          classifiers=[
              'Intended Audience :: Science/Research',
              'Programming Language :: Python :: 3.6',
              'License :: OSI Approved :: MIT License',
              'Topic :: Scientific/Engineering :: Astronomy',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS'],
      )
