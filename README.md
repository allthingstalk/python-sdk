# python-sdk

[![PyPI](https://img.shields.io/pypi/v/allthingstalk.svg)](https://pypi.python.org/pypi/allthingstalk)

AllThingsTalk Python SDK provides Python APIs to manage and implement AllThingsTalk devices.

## System Requirements

AllThingsTalk Python SDK is a Python 3 library, so make sure you have Python 3 installed. Python 2 won’t work.

## Installation

```
sudo pip3 install allthingstalk
```

> This will only install the sdk itself, not including any examples. If you want the sdk as well as some basic examples and experiments, clone the repository to a folder on your Raspberry Pi
`git clone https://github.com/allthingstalk/python-sdk`

## Examples

To run a very first basic example with AllThingsTalk

* Go to the _examples_ folder and open the _counter.py_ example using `sudo nano counter.py`
* Enter _deviceId_ and _auth token_ from your AllThingsTalk device
  ```
  DEVICE_TOKEN = 'IizOe18ktm3SQ7dGwwh8IPba'
  DEVICE_ID = 'maker:4HkDdSUrorhNW1VeVyvyeKGeszn1w8w2oAvJrEf8'
  ```
* Save and exit
* Run the example with `python3 counter.py`

## Documentation

https://allthingstalk.github.io/python-sdk/

# License

Apache 2.0

# Contributions

Pull requests and new issues are welcome.
