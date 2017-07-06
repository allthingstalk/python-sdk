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
# Note: DEVICE_TOKEN and DEVICE_ID are found on maker.allthingstalk.com
deviceToken = 'maker:4ObWht29bfsnW1VeVzx9yeXy1X5wWAtRUDPt6YK0'
deviceId = 'StsNx5D2Y5GPe1NZjmBb3N61'

# Create your Light Sensor device with light asset and set lx as a measuring unit (Lux)
class LightSensor(Device):
    light = NumberAsset(unit='lx')

# Authorize and connect your device with cloud
client = Client(deviceToken)
device = LightSensor(client=client, id=deviceId)

# Pin number on your shield where light sensor is connected
lightSensorPin = 0

# Light sensor's pin needs to be in INPUT mode
grovepi.pinMode(lightSensorPin, 'INPUT')

# Run as long as the device is turned on
while True:
	# Read state of the light sensor
    lightValue = grovepi.analogRead(lightSensorPin)
    # Send value from light sensor to the cloud
    device.light = lightValue
    # Log the value to standard output
    print('LightSensor value: %s' % lightValue)
    # Sleep for 1 second then do it all over again
    time.sleep(1)




