.. AllThingsTalk Python SDK documentation master file, created by
   sphinx-quickstart on Wed Apr 26 14:08:42 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _index:

AllThingsTalk Python SDK
========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

AllThingsTalk Python SDK is designed to offer easy programmatic access to `AllThingsTalk Platform <https://maker.allthingstalk.com/>`_. You can use it to implement AllThingsTalk devices on you computer, or on an embedded device like a Raspberry PI.

Here's a very simple example to whet your appetite: ::

  import random
  import time

  from allthingstalk import Client, Device, IntegerAsset

  class RandomDevice(Device):
      random_number = IntegerAsset()

  client = Client('your_device_token')
  device = RandomDevice(client=client, id='your_device_id')

  while True:
      device.random_number = random.randint(1, 100)
      time.sleep(1)

This code creates an asset named `random_number` on the device identified by `your_device_id`, using `your_device_token`. When that's done, it repeatedly sets the asset's value to random numbers between 1 and 100.

Installation
============

AllThingsTalk Python SDK is a Python 3 library, so make sure you `have Python 3 installed <https://www.python.org/downloads>`_. Python 2 won't work.

With PIP
--------

To install AllThingsTalk Python SDK, run this command in your terminal of choice: ::

  $ pip install allthingstalk

This is the preferred way of obtaining AllThingsTalk SDK.

From the source
---------------

.. note:: This is somewhat advanced. Don't use if installing with PIP will do.

AllThingsTalk SDK is developed in the open `on GitHub <https://github.com/allthingstalk/python-sdk>`_, where the code is always available.

You can clone the public repository with this command: ::

  $ git clone git://github.com/allthingstalk/python-sdk.git

Or, download the tarball: ::

  $ curl -OL https://github.com/allthingstalk/python-sdk/tarball/master
  # optionally, zipball is also available (for Windows users).

Once you have a copy of the source, you can embed it in your own Python package, or install it into your site-packages easily with: ::

  $ python setup.py install

Tutorial
========

Some python knowledge *is* going to be required for using the SDK, but you should be OK with the basics. If you have no prior experience with programming in Python, you should check out `The Python Tutorial <https://docs.python.org/3/tutorial/index.html>`_.

Defining devices
----------------

Device definition takes design cues from Django models. If you are familiar with that - awesome, you'll feel right at home - if not, don't worry, you'll be grokking them in no time. Let's do another example and look at it more closely.

.. _weather-station:

::

  class WeatherStation(Device):
      temperature = NumberAsset(unit='°C')
      forecast = StringAsset(kind=Asset.VIRTUAL)
      reset = BooleanAsset(kind=Asset.ACTUATOR)

Each device you create will subclass AllThingsTalk :class:`Device <allthingstalk.Device>`. Device assets are defined as class attributes.

.. note:: In the examples, it's assumed that all of `allthingstalk` is imported into the current package, i.e. ``from allthingstalk import *``.

We're defining a device called `WeatherStation`, which has three assets: `temperature`, `forecast`, and `reset`. At this moment, we are not concerning ourselves with how their values are going to be obtained, but how they are going to be modeled in AllThingsTalk Platform.

The assets in this example have different types: :class:`NumberAsset <allthingstalk.NumberAsset>`, :class:`StringAsset <allthingstalk.StringAsset>`, and :class:`BooleanAsset <allthingstalk.BooleanAsset>`. To see other available asset types, you can jump to :ref:`Assets <api-assets>`. They are also of different `kinds <http://docs.allthingstalk.com/cloud/concepts/assets/#types>`_. `Temperature` is a ``SENSOR``, which is the default asset kind, `forecast` is a ``VIRTUAL``, and `reset` is an ``ACTUATOR``.

Some asset types, like :class:`NumberAsset <allthingstalk.NumberAsset>`, can be configured with type specific properties - extras [#extras]_. Here, we're configuring `temperature's` ``unit`` to ``'°C'``, so that there's no ambiguity about the chosen temperature scale [#temp_unit]_.

Connecting to the cloud
-----------------------

The :ref:`WeatherStation <weather-station>` we just defined won't do anything on its own. It needs to be able to connect to the cloud and bind itself to a device resource identified by an `id`.

To make this happen, we need to use a :ref:`client <api-clients>` with a `WeatherStation` instance.

::

   client = Client('your_token')
   weather = WeatherStation(client=client, id=id)

Once ``weather`` is initialized, the SDK will take the assets from `WeatherStation` definition and use them to configure the device's assets on the Platform. If `id` is not supplied, a new device will be created first.

.. warning:: Not all clients can create devices. In general, you shouldn't assume that all of :class:`BaseClient <allthingstalk.BaseClient>` methods will be implemented by a given client. Also, when using :class:`Client <allthingstalk.Client>` - which does implement most of the client methods - you should keep in mind that the supplied token might not offer sufficient permissions.

By default a :class:`AssetMismatchException <allthingstalk.AssetMismatchException>` will be thrown if there's a type or kind mismatch between the existing assets on the Platform and the assets defined for the device identified by the same name. To overwrite existing assets, initialize the device with ``overwrite_assets=True`` ::

  weather = WeatherStation(client=client, id=id, overwrite_assets=True)

Postponed connection
^^^^^^^^^^^^^^^^^^^^

If you don't want to connect immediately after creating a device, you can set ``connect`` argument to ``False``, and use the device's :class:`connect <allthingstalk.Device.connect>` method to connect later. All the arguments available to :class:`Device <allthingstalk.Device>` initializers are available to connect as well. ::

  weather = WeatherStation(client=client, id=id, connect=False)
  ...
  # other code
  ...
  weather.connect()

Adding assets
-------------

During device development, you might need to append assets to a device after it's been created. Doing this is as simple as stopping the program, extending the device class with the needed assets (in this case `humidity` and `alert`) and restarting.

.. code-block:: python
   :emphasize-lines: 3,4

   class WeatherStation(Device):
       temperature = NumberAsset(unit='°C')
       humidity = NumberAsset(unit='%')
       alert = BooleanAsset()
       forecast = StringAsset(kind=Asset.VIRTUAL)
       reset = BooleanAsset(kind=Asset.ACTUATOR)

Publishing values
-----------------

Once your device is connected, you're ready to publish values to the Platform. To publish a value to an asset resource and set its state, simply assign the value to the corresponding field of your :class:`Device <allthingstalk.Device>` instance. ::

  weather.temperature = 21.3
  weather.humidity = 3.1
  weather.alert = False

There is no special "device loop". You can use pure Python and any of the awesome Python libraries to implement your business logic. For example, with `GrovePi Temperature and Humidity Sensor Pro <http://wiki.seeed.cc/Grove-Temperature_and_Humidity_Sensor_Pro/>`_, you could implement the `WeatherDevice` for real as simply as: ::

  ...

  while True:
      temperature, humidity = grovepi.dht(SENSOR_PIN, 1)
      weather.temperature = temperature
      weather.humidity = humidity
      time.sleep(1)

  ...

Listening to commands
---------------------

To listen for commands from `reset` actuator, do the following: ::

   @WeatherStation.command.reset
   def on_reset(device, value, at):
       reset_my_weather_station()


Listening to feeds
------------------

If you'd like to implement a separate program to listen to feeds coming from the weather station, specifically from `temperature` sensor: ::

   @WeatherStation.feed.temperature
   def on_reset(device, value, at):
       print('Received %s at %s' % (value, at))

---------------

API Reference
=============

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

.. rubric:: Footnotes

.. [#extras] Each predefined asset type maps to a predefined asset :ref:`profile <api-profiles>`, which in turn maps to `AllThingsTalk asset profiles <http://docs.allthingstalk.com/cloud/concepts/assets/profiles/>`_.
.. [#temp_unit] Defining the temperature scale is of course optional - the platform will work just fine without it. Nevertheless, specifying units for physical measures is a good practice, and as a bonus, we'll be able to see the ``unit`` on the Platform interface.
