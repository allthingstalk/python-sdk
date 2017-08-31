:ref:`Back to index <index>`

API
===

.. module:: allthingstalk

This part of the documentation covers all the interfaces of AllThingsTalk SDK.

.. _api-assets:

Assets
------

.. autoclass:: Asset
   :members:

   .. automethod:: __init__

.. autoclass:: NumberAsset
   :members:

.. autoclass:: IntegerAsset
   :members:

.. autoclass:: StringAsset
   :members:

.. autoclass:: BooleanAsset
   :members:

.. autoclass:: GeoAsset
   :members:

.. _api-clients:

Asset State
-----------

.. autoclass:: AssetState
   :members:

   .. automethod:: __init__

Clients
-------

.. autoclass:: BaseClient
   :members:

.. autoclass:: Client
   :members:

   .. automethod:: __init__

.. _api-devices:

Devices
-------

.. autoclass:: Device
   :members:

   .. automethod:: __init__

.. _api-exceptions:

Exceptions
----------

.. autoexception:: AssetMismatchException

.. autoexception:: AssetStateRetrievalException

.. autoexception:: AccessForbiddenException

.. autoexception:: InvalidAssetProfileException

.. _api-profiles:

Profiles
--------

.. autoclass:: allthingstalk.profiles.Profile
   :members:

.. autoclass:: allthingstalk.profiles.NumberProfile
   :members:

.. autoclass:: allthingstalk.profiles.IntegerProfile
   :members:

.. autoclass:: allthingstalk.profiles.BooleanProfile
   :members:

.. autoclass:: allthingstalk.profiles.StringProfile
   :members:

.. autoclass:: allthingstalk.profiles.ObjectProfile
   :members:

.. autoclass:: allthingstalk.profiles.GeoProfile
   :members:

:ref:`Back to index <index>`
