# python-sdk

[![PyPI](https://img.shields.io/pypi/v/allthingstalk.svg)](https://pypi.python.org/pypi/allthingstalk)

AllThingsTalk Python SDK provides Python APIs to manage and implement AllThingsTalk devices.

## System Requirements

AllThingsTalk Python SDK is a Python 3 library, so make sure you have Python 3 installed. Python 2 won’t work.

## Installation

### Using pip

The SDK is available on [PyPI](https://pypi.python.org/pypi), and can be installed using `pip3`. If you don't have `pip3` or `python3` installed, please follow the [Python Installation Tutorial](http://docs.python-guide.org/en/latest/starting/installation/).

```
pip3 install allthingstalk
```

We recommend that you install the SDK inside a [Python Virtual Enviroment](https://realpython.com/blog/python/python-virtual-environments-a-primer/). In case you wish to install the package globally, you will probably need to prefix the command with `sudo`.

### From source code

It's also possible to install AllThingsTalk Python SDK from source code.

You can either clone the public repository:

```
git clone git://github.com/allthingstalk/python-sdk.git
```

Or, download the [tarball](https://github.com/allthingstalk/requests/tarball/master):

```
curl -OL https://github.com/allthingstalk/requests/tarball/master
```

To install the package, use:

```
cd python-sdk
pip3 install .
```

### On a Raspberry PI

One of primary use cases for the AllThingsTalk Python SDK is embedded development on Linux devices, and Raspberry PI is among the most popular embedded Linux platforms.

To install the SDK, you can use any of the methods above. Whichever method you choose, we recommend executing it globally as a super user - `sudo pip3 install allthingstalk`.

To see how to integrate the SDK with Grove PI sensors, please take a look at [Using AllThingsTalk SDK with GrovePi](examples/grovepi/README.md).

## Examples

To obtain examples you can either clone the repository as described above, or copy the examples directly from GitHub.

[Counter](examples/counter.py) is one of the most basic examples. Copy it to your hard drive, and replace `DEVICE_TOKEN` and `DEVICE_ID` with those obtained from [Maker](https://maker.allthingstalk.com). If you have installed the SDK correctly, you should be able to run the example with `python3 counter.py`. The example will create one asset and increment it from `0` to `9` with second long delays. You can use Maker to monitor the progress.

## Documentation

https://allthingstalk.github.io/python-sdk/

# License

Apache 2.0

# Contributions

Pull requests and new issues are welcome.
