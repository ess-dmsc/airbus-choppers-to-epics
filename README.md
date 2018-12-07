# Airbus Choppers to EPICS

## Installation
Uses Python 3.

```python
>>> pip install -r requirements.txt
```

### OSX Woes

It is a bit of a pain in the arse to install pcaspy on MacOS:
```python
>>> brew install swig
>>> export EPICS_BASE=/opt/epics/base
>>> export EPICS_HOST_ARCH=darwin-x86
>>> pip install pcaspy
```
