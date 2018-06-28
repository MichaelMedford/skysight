#! /usr/bin/env python
#

DESCRIPTION = "A package for testing the properties of astronomical dither patterns"
DISTNAME = 'dither'
AUTHOR = 'Michael Medford'
MAINTAINER = 'Michael Medford' 
MAINTAINER_EMAIL = 'MichaelMedford@berkeley.edu'
URL = 'https://github.com/MichaelMedford/dither'
LICENSE = 'MIT License'
import dither
VERSION = dither.__version__

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
          packages=['dither'],
          package_data={'dither': ['data/*']},
          classifiers=[
              'Intended Audience :: Science/Research',
              'Programming Language :: Python :: 3.6',
              'License :: OSI Approved :: MIT License',
              'Topic :: Scientific/Engineering :: Astronomy',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS'],
      )
