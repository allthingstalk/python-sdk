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
# AllThingsTalk Doorbell experiment
#
# Before running this experiment, make certain that grovepi3 and allthingstalk
# libraries are installed and globally accessible.
#

import time
import grovepi
from allthingstalk import Device, BooleanAsset, Client

# Parameters used to authorize and identify your device
# Note: DEVICE_TOKEN and DEVICE_ID are found on maker.allthingstalk.com
deviceToken = '<DEVICE_TOKEN>'
deviceId = '<DEVICE_ID>'

# Create your Smart Doorbell device with button asset
class SmartDoorbell(Device):
    button = BooleanAsset()

# Authorize and connect your device with cloud
client = Client(deviceToken)
device = SmartDoorbell(client=client, id=deviceId)

# Pin number on your shield where button is connected
buttonPin = 2

# Button's pin needs to be in INPUT mode
grovepi.pinMode(buttonPin, 'INPUT')

previousButtonState = False

# Run as long as the device is turned on
while True:
    # Read state of the button
    buttonState = grovepi.digitalRead(buttonPin)
    if buttonState == 1:
    	if previousButtonState == False:
    		# Send True value to the cloud, indicating that button is pressed
    		device.button = True
    		# Log change to standard output
    		print( "Dorbell is activated" )
    		previousButtonState = True
    elif previousButtonState == True:
    	# Send False value to the cloud, indicating that button is released
    	device.button = False
    	# Log change to standard output
    	print( "Dorbell is deactivated" )
    	previousButtonState = False
    # Sleep for .3 seconds then do it all over again
    time.sleep(.3)





