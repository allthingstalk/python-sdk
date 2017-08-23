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
# AllThingsTalk LED Actuator experiment
#
# Before running this experiment, make certain that grovepi3 and allthingstalk
# libraries are installed and globally accessible.
#

import time
import RPi.GPIO as GPIO
from allthingstalk import Device, BooleanAsset, Client, Asset

# Parameters used to authorize and identify your device
# Get them on maker.allthingstalk.com
DEVICE_TOKEN = '<DEVICE_TOKEN>'
DEVICE_ID = '<DEVICE_ID>'


class LedActuator(Device):
    led = BooleanAsset(kind=Asset.ACTUATOR)


# Authorize and connect your device with the Cloud
client = Client(DEVICE_TOKEN)
device = LedActuator(client=client, id=DEVICE_ID)

# LED is connected to GPIO4
led_pin = 4

# Led's pin needs to be in OUTPUT mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)


@LedActuator.command.led
def on_led(device, value, at):
    # Turn led On or Off depending on the received Command
    GPIO.output(led_pin, value)

    # Send value to the cloud to reflect physical state of the led
    device.led = value

    print('Led state updated to %s.' % value)


while True:
    print('Waiting for actuation...')
    time.sleep(5)
