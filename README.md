# Airbus Choppers to EPICS

## Installation

It is a bit of a pain in the arse to install pcaspy on MacOS:
```python
>>> brew install swig
>>> export EPICS_BASE=/opt/epics/base
>>> export EPICS_HOST_ARCH=darwin-x86
>>> pip install pycaspy
```

The rest can be installed like so:
```python
>>> pip install -r requirements.txt
```
