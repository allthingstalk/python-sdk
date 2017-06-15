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

from . import profiles


class Asset:

    SENSOR = 'sensor'
    ACTUATOR = 'actuator'
    CONFIG = 'config'
    VIRTUAL = 'virtual'

    _PROFILE_CLASS = None

    def __init__(self, *, kind='sensor', name=None, title=None,
                 description='', handler=None, **kwargs):
        self.id = None
        self.thing_id = None
        self.kind = kind if kind else 'sensor'
        self.name = name
        self._internal_id = name
        self.title = title or name
        self.description = description
        self.handler = handler
        if self.__class__._PROFILE_CLASS:
            self.profile = self.__class__._PROFILE_CLASS(**kwargs)
        elif 'profile' in kwargs and kwargs['profile']:
            self.profile = kwargs['profile']
        if 'type' in self.profile:
            self.type = self.profile['type']


class NumberAsset(Asset):
    _PROFILE_CLASS = profiles.NumberProfile


class IntegerAsset(NumberAsset):
    _PROFILE_CLASS = profiles.IntegerProfile


class StringAsset(Asset):
    _PROFILE_CLASS = profiles.StringProfile


class BooleanAsset(Asset):
    _PROFILE_CLASS = profiles.BooleanProfile


class GeoAsset(Asset):
    _PROFILE_CLASS = profiles.GeoProfile
