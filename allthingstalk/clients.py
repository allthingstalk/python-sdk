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

import logging

import paho.mqtt.client as paho_mqtt
import requests

logger = logging.getLogger('allthingstalk')


class BaseClient:
    '''BaseClient is a base class used for implementing AllThingsTalk Platform
    clients, which are used for interfacing the SDK code with the Platform. It
    doesn't implement any of the client methods.'''

    def _attach_device(self, device):
        pass

    def get_assets(self, device_id):
        raise NotImplementedError('get_assets not implemented')

    def create_asset(self, device_id, asset):
        raise NotImplementedError('create_asset not implemented')

    def publish_asset_state(self, device_id, asset_name, value):
        raise NotImplementedError('publish_asset_state not implemented')


class Client(BaseClient):

    def __init__(self, token, *, api='api.allthingstalk.io',
                 http=None, mqtt=None):
        self.token = token

        def prefix_http(url):
            return url if url.startswith('http') else 'https://%s' % url

        if api.startswith('http://') or api.startswith('https://'):
            api = api.split('//', 1)[1]

        # HTTP Client
        if http:
            self.http = prefix_http(http)
        elif api:
            self.http = prefix_http(api)
        else:
            raise ValueError('Either api or http must be set.')

        # MQTT Client
        if mqtt:
            if ':' in mqtt:
                host, port = mqtt.split(':')[:2]
            else:
                host, port = mqtt, '1883'
            self.mqtt = self._make_mqtt_client(host, port, token)
        elif api:
            host, port = host, port = api, '1883'
            self.mqtt = self._make_mqtt_client(host, port, token)
        else:
            self.mqtt = None

        self._devices = {}

    def _make_mqtt_client(self, host, port, token):
        def on_mqtt_connect(client, userdata, rc):
            logger.debug('MQTT client connected to %s:%s' % (host, port))

        def on_mqtt_disconnect(client, userdata, rc):
            logger.debug('MQTT client disconnected with status %s' % rc)

        def on_mqtt_subscribe(client, userdata, mid, granted_qos):
            pass

        def on_mqtt_message(client, userdata, message):
            logger.debug('MQTT client received a message on topic "%s": %s'
                         % (message.topic, message.payload))
            parts = message.topic.split('/')
            _, device_id, _, asset_name, stream = parts
            self._devices[device_id]._on_message(stream, asset_name, message.payload)

        client = paho_mqtt.Client()
        client.username_pw_set(token, token)
        client.on_connect = on_mqtt_connect
        client.on_disconnect = on_mqtt_disconnect
        client.on_message = on_mqtt_message
        client.on_subscribe = on_mqtt_subscribe
        client.connect(host, int(port), 60)
        client.loop_start()
        return client

    def _attach_device(self, device):
        if self.mqtt:
            logger.debug('Client %s attaching device %s' % (self, device.id))
            for action in ['feed', 'command']:
                logger.debug('Subscribing to %s\'s %ss' % (device.id, action))
                self.mqtt.subscribe('device/%s/asset/+/%s' % (device.id, action))
        self._devices[device.id] = device

    def get_assets(self, device_id):
        return requests.get('%s/device/%s/assets' % (self.http, device_id),
                            headers={'Authorization': 'Bearer %s' % self.token}).json()

    def create_asset(self, device_id, asset):
        attalk_asset = {
            'Name': asset.name,
            'Title': asset.title,
            'Description': asset.description,
            'Is': asset.kind,
            'Profile': asset.profile
        }
        return requests.post('%s/device/%s/assets' % (self.http, device_id),
                             headers={'Authorization': 'Bearer %s' % self.token},
                             json=attalk_asset).json()

    def publish_asset_state(self, device_id, asset_name, value):
        requests.put('%s/device/%s/asset/%s/state' % (self.http, device_id, asset_name),
                     headers={'Authorization': 'Bearer %s' % self.token},
                     json={'value': value})

    def __del__(self):
        try:
            self.mqtt.loop_stop(force=True)
        except:
            pass
