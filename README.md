# Airbus Choppers to EPICS

## Installation
Uses Python 3.

It is a bit of a pain in the arse to install pcaspy, for example: on MacOS:
```python
>>> brew install swig
>>> export EPICS_BASE=/opt/epics/base
>>> export EPICS_HOST_ARCH=darwin-x86
>>> pip install pcaspy
```
Hopefully, for Windows it is possible to copy the `bin` directory from a Windows build of EPICS and just modify the above command appropriately. Might be worth seeing what IBEX do as their genie_python has all the pcaspy stuff included.

The rest can be installed like so:
```python
>>> pip install -r requirements.txt
```
