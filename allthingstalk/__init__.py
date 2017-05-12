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

'''
AllThingsTalk SDK
~~~~~~~~~~~~~~~~~

:copyright: (c) 2017 by AllThingsTalk
:license: Apache 2.0, see LICENSE for more details.
'''

__title__ = 'allthingstalk'
__version__ = '0.1.0'
__author__ = 'Danilo Vidovic'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 AllThingsTalk'

from .assets import *
from .clients import BaseClient, Client
from .devices import Device
from .exceptions import AssetMismatchException
