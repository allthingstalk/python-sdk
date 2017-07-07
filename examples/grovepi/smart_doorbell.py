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
# AllThingsTalk Doorbell experiment
#
# Before running this experiment, make certain that grovepi3 and allthingstalk
# libraries are installed and globally accessible.
#

import time
import grovepi
from allthingstalk import Device, BooleanAsset, Client

# Parameters used to authorize and identify your device
# Get them on maker.allthingstalk.com
DEVICE_TOKEN = '<DEVICE_TOKEN>'
DEVICE_ID = '<DEVICE_ID>'


class SmartDoorbell(Device):
    '''A smart doorbell's interface to the user is a button.
    This button is modeled as a boolean sensor.'''
    button = BooleanAsset()


# Authorize and connect your device with cloud
client = Client(DEVICE_TOKEN)
device = SmartDoorbell(client=client, id=DEVICE_ID)

# Pin number on your shield where button is connected
button_pin = 2

# Button's pin needs to be in INPUT mode
grovepi.pinMode(button_pin, 'INPUT')

# While pressed, the button sensor will send 1 (one).
# We don't want to send these ones as separate button
# presses, so we need to keep track of the previous
# button state - when it's True, it means that the button
# was pressed already, and that we don't need to send
# more data. When it was False, and we receive a one,
# it means that the button has just been pressed and
# data needs to be sent to the Cloud.
previous_button_state = False

# Run as long as the device is turned on
while True:
    # Read state of the button
    button_state = grovepi.digitalRead(button_pin)
    if button_state == 1:
        if not previous_button_state:
            # Send True value to the cloud, indicating that
            # button is pressed.
            device.button = True
            # Log change to standard output
            print('Dorbell activated.')
            previous_button_state = True
    # When button is released, we publish that only once as well.
    elif previous_button_state:
        # Send False value to the cloud, indicating that
        # button is released.
        device.button = False
        # Log change to standard output
        print('Dorbell deactivated.')
        previous_button_state = False

    # Sleep for 0.3 seconds then do it all over again
    time.sleep(0.3)
