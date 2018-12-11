# Airbus Choppers to EPICS

## Installation
Python 2.7 only.

The application can be installed like so:
```python
>>> pip install -r requirements.txt
```

To run:
```python
>>> python main.py
```

It may be necessary to specify which network interface to listen on first though:
```python
>>> set EPICS_CAS_INTF_ADDR_LIST=X.X.X.X
```