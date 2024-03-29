# skysight
A package for determining the optimal astronomical dither strategy

# Installation

This installation assumes that you have a copy of conda installed and in 
your PATH. Navigate to the directory where you want to save this 
folder. Then execute:
```bash
git clone https://github.com/MichaelMedford/skysight.git
cd skysight
conda install --yes --file requirements.txt
python setup.py install
```

# Testing

Confirm that all packages are correctly installed.
```bash
python test/print_versions.py
```
Run tests to make sure that everything is working correctly.
```bash
python setup.py test
```

# Requirements
* Python 3.6

# Authors
* Michael Medford <MichaelMedford@berkeley.edu>

# Citation
[![DOI](https://zenodo.org/badge/139060412.svg)](https://zenodo.org/badge/latestdoi/139060412)
