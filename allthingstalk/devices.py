#    _   _ _ _____ _    _              _____     _ _     ___ ___  _  __
#   /_\ | | |_   _| |_ (_)_ _  __ _ __|_   _|_ _| | |__ / __|   \| |/ /
#  / _ \| | | | | | ' \| | ' \/ _` (_-< | |/ _` | | / / \__ \ |) | ' <
# /_/ \_\_|_| |_| |_||_|_|_||_\__, /__/ |_|\__,_|_|_\_\ |___/___/|_|\_\
#                             |___/
#
# Copyright 2017 AllThingsTalk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__all__ = ['Device']

import datetime
from dateutil.parser import parse as parse_date

import json
import copy

from . import assets


# inspired by https://github.com/django/django/blob/master/django/db/models/base.py
class DeviceBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__

        # Only perform for Device subclases (not Device class itself)
        parents = [b for b in bases if isinstance(b, DeviceBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        new_attrs = {'__module__': attrs.pop('__module__')}

        # Python 3.6 support:  http://stackoverflow.com/questions/41343263
        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell
        new_class = super_new(cls, name, bases, new_attrs)

        #
        # Class enhancements
        #

        # Message handlers for state / feed / command / event

        new_class._handlers = {}
        new_class.state = DeviceBase.HandlerDecoratorCollection(new_class, 'state')
        new_class.feed = DeviceBase.HandlerDecoratorCollection(new_class, 'feed')
        new_class.command = DeviceBase.HandlerDecoratorCollection(new_class, 'command')
        new_class.event = DeviceBase.HandlerDecoratorCollection(new_class, 'event')

        # Asset transformations
        for name, asset in attrs.items():
            if isinstance(asset, assets.Asset):
                # Configure asset name from variable name
                if not asset.name:
                    asset.name = name
                if not asset.title:
                    asset.title = name.capitalize()
                asset._internal_id = name

                # Create the actuation decorator
                new_class.state._add_asset(asset)
                new_class.feed._add_asset(asset)
                new_class.command._add_asset(asset)
                new_class.event._add_asset(asset)

        new_class._assets = [value for name, value in attrs.items()
                             if isinstance(value, assets.Asset)]

        return new_class

    class HandlerDecoratorCollection:

        def __init__(self, device_class, stream):
            device_class._handlers[stream] = {}
            self._stream = stream
            self._device_class = device_class
            self._assets = {}

        def _add_asset(self, asset):
            def decorator(fn):
                self._device_class._handlers[self._stream][asset._internal_id] = fn
                return fn
            self._assets[asset._internal_id] = decorator

        def __getattr__(self, internal_id):
            if internal_id in self._assets:
                return self._assets[internal_id]
            else:
                return AttributeError


class Device(metaclass=DeviceBase):
    '''Device contains information about assets. It maps to AllThingsTalk
    Platform device resources.'''

    def __init__(self, *, client=None, id=None, connect=True,
                 overwrite_assets=False, **kwargs):
        '''Initializes the device

        :param Client client: The client used to interface with the platform
        :param str id: Device resource id. If supplied, the device will be mapped to the device resource. If None, an attempt will be made to create the device.
        :param connect boolean: If ``True``, the device should connect to the cloud immediately.
        :param bool overwrite_assets: If ``True``, asset mismatch between the Platform and device definition will be resolved by configuring local assets on the Platform. If ``False``, AssetMismatchException will be raised.

        :raises AssetMismatchException: if asset mismatch is found between the existing asset on the Platform and an asset definition, and overwrite_assets is ``False``

        '''

        self._connected = False

        self.id = id
        self.client = client

        self.overwrite_assets = overwrite_assets
        self.assets = {asset._internal_id: copy.copy(asset) for asset in self._assets}

        def make_get_asset(asset):
            def getter(self):
                print(asset)
                return self.client
            return getter

        def make_set_asset(asset):
            def setter(self, value):
                if self._connected:
                    self.client.publish_asset_state(self.id, asset.name, value)
                else:
                    raise RuntimeError('Device not started.')
            return setter

        for asset in self.assets.values():
            asset_property = property(
                make_get_asset(asset), make_set_asset(asset), None,
                asset.description or asset.name or asset._internal_id)
            setattr(type(self), asset._internal_id, asset_property)

        if connect and client:
            self.connect()

    def connect(self, *, client=None, id=None, overwrite_assets=None):
        '''Connects to the device to AllThingsTalk Platform

        :param Client client: The client used to interface with the platform
        :param str id: Device resource id. If supplied, the device will be mapped to the device resource. If None, an attempt will be made to create the device.
        :param bool overwrite_assets: If ``True``, asset mismatch between the Platform and device definition will be resolved by configuring local assets on the Platform. If ``False``, AssetMismatchException will be raised.

        :raises AssetMismatchException: if asset mismatch is found between the existing asset on the Platform and an asset definition, and overwrite_assets is ``False``
        '''

        if id is not None:
            self.id = id
        if client is not None:
            self.client = client
        if overwrite_assets is not None:
            self.overwrite_assets = overwrite_assets

        if not self.id:
            raise NotImplementedError('Device creation not implemented.')

        cloud_assets = {asset['name']: asset for asset in self.client.get_assets(self.id)}
        for name, asset in self.assets.items():
            if name in cloud_assets:
                asset.id = cloud_assets[name]['id']
                asset.thing_id = cloud_assets[name]['deviceId']
            else:
                new_cloud_asset = self.client.create_asset(self.id, asset)
                asset.id = new_cloud_asset['id']
                asset.thing_id = new_cloud_asset['deviceId']

        self.client._attach_device(self)
        self._connected = True

    def _on_message(self, stream, internal_asset_id, message):
        if internal_asset_id in self._handlers[stream]:
            msg = json.loads(message)
            if isinstance(msg, dict):
                msg = {k.lower(): v for k, v in msg.items()}
            else:
                msg = {'value': msg}
            if 'at' in msg and msg['at'] is not None:
                at = parse_date(msg['at'])
            else:
                at = datetime.datetime.utcnow()
            value = msg['value']
            self._handlers[stream][internal_asset_id](self, value, at)
