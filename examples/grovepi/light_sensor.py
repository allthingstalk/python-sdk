#!/usr/bin/env python3

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

#
# AllThingsTalk Light sensor experiment
#
# Before running this experiment, make certain that grovepi3 and allthingstalk
# libraries are installed and globally accessible.
#

import time
import grovepi
from allthingstalk import Device, NumberAsset, Client

# Parameters used to authorize and identify your device
# Get them on maker.allthingstalk.com
DEVICE_TOKEN = '<DEVICE_TOKEN>'
DEVICE_ID = '<DEVICE_ID>'


class LightSensor(Device):
    '''Light sensing device with a single asset that measures
    illuminance.'''
    light = NumberAsset(unit='lx')  # lx stands for Lux


# Authorize and connect your device with the Cloud
client = Client(DEVICE_TOKEN)
device = LightSensor(client=client, id=DEVICE_ID)

# Pin number on your shield where light sensor is connected
light_sensor_pin = 0

# Light sensor's pin needs to be in INPUT mode
grovepi.pinMode(light_sensor_pin, 'INPUT')

# Run as long as the device is turned on
while True:
    # Read state of the light sensor
    light_value = grovepi.analogRead(light_sensor_pin)
    # Send value from light sensor to the cloud
    device.light = light_value
    # Log the value to standard output
    print('Light sensor value: %s' % light_value)
    # Sleep for 1 second then do it all over again
    time.sleep(1)
