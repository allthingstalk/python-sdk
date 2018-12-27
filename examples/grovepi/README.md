# Using AllThingsTalk SDK with GrovePi

## System Requirements

AllThingsTalk Python SDK is a Python 3 library, so make sure you have Python 3 installed. Python 2 won’t work.

## Installation

### Install GrovePi library for Python 3

The quickest way for installing the GrovePi is to enter the following command:


```
curl -kL dexterindustries.com/update_grovepi | bash
```

```
sudo pip install grovepi
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
