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
# AllThingsTalk Motion detector experiment
#
# Before running this experiment, make certain that grovepi3 and allthingstalk
# libraries are installed and globally accessible.
#

import time
import grovepi
from allthingstalk import Device, BooleanAsset, Client, Asset

# Parameters used to authorize and identify your device
# Get them on maker.allthingstalk.com
DEVICE_TOKEN = '<DEVICE_TOKEN>'
DEVICE_ID = '<DEVICE_ID>'


class MotionDetector(Device):
    '''Motion sensing device consisting of a motion sensor represented as
    a boolean asset, and an LED that can be actuated from the Cloud.'''
    motion_sensor = BooleanAsset()
    led = BooleanAsset(kind=Asset.ACTUATOR)


# Authorize and connect your device with the Cloud
client = Client(DEVICE_TOKEN)
device = MotionDetector(client=client, id=DEVICE_ID)

# Pin numbers on your shield where motion sensor and led are connected
motion_sensor_pin = 3
led_pin = 4

# Motion sensor's pin needs to be in INPUT mode
grovepi.pinMode(motion_sensor_pin, 'INPUT')
# Led's pin needs to be in OUTPUT mode
grovepi.pinMode(led_pin, 'OUTPUT')


# Setup listener for commands sent from the Cloud for your LED
@MotionDetector.command.led
def on_led(device, value, at):
    if value:
        # If command is True set value 1 on led pin, turning the led on
        grovepi.digitalWrite(led_pin, 1)
        # Send value to the cloud to reflect physical state of the led
        device.led = True
    else:
        # If command is other than True set value 0 on led pin, turning led off
        grovepi.digitalWrite(led_pin, 0)
        # Send value to the cloud to reflect physical state of the led
        device.led = False

    print('Led state updated.')


# Motion sensor will send 1 (one) every time it detects motion.
# For continuous motion, it will send many ones. We don't want to
# send multiple state updates for a single movement, even if it
# lasts for a few seconds - instead, we'd like to be able to tell
# when separate movement sequences occur. This is why we need to
# keep track of movements and be able to tell if data received from
# the sensor is only indicating a continuation of an already identified
# movement, or if it marks the start of a new motion that we want
# to send to the Cloud.
previous_motion_sensor_state = False

# Run as long as the device is turned on
while True:
    # Read state of the motion sensor sensor
    motion_sensor_state = grovepi.digitalRead(motion_sensor_pin)
    if motion_sensor_state == 1:
        # Let's just publish new motions:
        if not previous_motion_sensor_state:
            # Send True value to the cloud, indicating that motion sensor
            # has detected movement.
            device.motion_sensor = True
            # Log change to standard output
            print('Motion detected.')
            previous_motion_sensor_state = True
    # When motion stops, we publish that only once as well.
    elif previous_motion_sensor_state:
        # Send False value to the cloud, indicating that motion sensor
        # has not detected movement.
        device.motion_sensor = False
        # Log change to standard output
        print('No more motion detected.')
        previous_motion_sensor_state = False

    # Sleep for 0.3 seconds then do it all over again
    time.sleep(0.3)
