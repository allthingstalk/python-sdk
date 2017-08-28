# Using AllThingsTalk SDK with GrovePi

## System Requirements

AllThingsTalk Python SDK is a Python 3 library, so make sure you have Python 3 installed. Python 2 won’t work.

## Installation

### Install GrovePi library for Python 3

Clone Dexter industries GrovePi repository to your Raspberry PI:

```
git clone https://github.com/DexterInd/GrovePi.git
```

Navigate to `GrovePi/Script` and run:

```
sudo sh ./grovepi_python3_install.sh
```

Navigate to `GrovePi/Software/Python` and run:

```
sudo pip3 install .
```

Reboot your Raspberry PI

```
sudo reboot
```

### Installing AllThingsTalk Python SDK

If you have `python3` and `pip3` install, run the following:

```
sudo pip3 install allthingstalk
```

## Running examples

To obtain examples you can either clone this repository as described in [README](../README.md), or copy the examples directly from GitHub.

Run them as a superuser using `python3`, after replacing `DEVICE_TOKEN` and `DEVICE_ID` in source code with those obtained from [Maker](https://maker.allthingstalk.com), for example:

```
sudo python3 ./light_sensor.py
```
