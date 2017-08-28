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

import datetime
import dateutil.tz
from dateutil.parser import parse as parse_date


class AssetState:
    """AssetState is used instead of primitive state values (like ``2``, ``"a"``
    or ``True``) when publishing data with a custom timestamp, i.e. not the
    current timestamp at the time of publishing."""

    def __init__(self, value, at=None):
        """Initializes the asset state.

        :param value: Any JSON-serializable value applicable to the given :class:`~allthingstalk.Asset`.
        :param datetime.datetime at: Optional timestamp
        """

        self.value = value
        if at is None:
            self.at = datetime.datetime.utcnow()
        elif isinstance(at, str):
            self.at = parse_date(at)
        elif isinstance(at, datetime.datetime):
            self.at = at
        else:
            raise ValueError('Invalid timestamp in at: %s' % at)

        if self.at.tzinfo is None:
            self.at = self.at.replace(tzinfo=dateutil.tz.tzutc())

    def __repr__(self):
        return 'AssetState(value=%s, at=%s)' % (self.value, self.at)

    def __str__(self):
        return str(self.value)
