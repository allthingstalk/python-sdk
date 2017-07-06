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
# Note: DEVICE_TOKEN and DEVICE_ID are found on maker.allthingstalk.com
deviceToken = 'maker:4ObWht29bfsnW1VeVzx9yeXy1X5wWAtRUDPt6YK0'
deviceId = 'StsNx5D2Y5GPe1NZjmBb3N61'

# Create your Motion detector device with motion sensor asset and diode asset (diode is set as actuator)
class MotionDetector(Device):
    motionSensor = BooleanAsset()
    diode = BooleanAsset(kind=Asset.ACTUATOR)

# Authorize and connect your device with cloud
client = Client(deviceToken)
device = MotionDetector(client=client, id=deviceId)

# Pin numbers on your shield where motion sensor and diode are connected
motionSensorPin = 3
diodePin = 4

# Motion sensor's pin needs to be in INPUT mode
grovepi.pinMode(motionSensorPin, "INPUT")
# Diode's pin needs to be in OUTPUT mode
grovepi.pinMode(diodePin, "OUTPUT")

previousMotionSensorState = False

# Setup listener for commands sent from cloud for your diode
@MotionDetector.command.diode
def on_diode(device, value, at):
    if value == True:
        # If command is True set value 1 on diode pin, turning diode on
        grovepi.digitalWrite(diodePin, 1)
        # Send value to the cloud to reflect physical state of the diode
        device.diode = True
    else:
        # If command is other than True set value 0 on diode pin, turning diode off
        grovepi.digitalWrite(diodePin, 0)
        # Send value to the cloud to reflect physical state of the diode
        device.diode = False

    print('Diode state is updated')

# Run as long as the device is turned on
while True:
    # Read state of the motion sensor sensor
    motionSensorState = grovepi.digitalRead(motionSensorPin)
    if motionSensorState == 1:
    	if previousMotionSensorState == False:
            # Send True value to the cloud, indicating that motion sensor detected movement
    		device.motionSensor = True
            # Log change to standard output
    		print( "Motion detected" )
    		previousMotionSensorState = True
    elif previousMotionSensorState == True:
        # Send False value to the cloud, indicating that motion sensor is not detecting any movement
    	device.motionSensor = False
        # Log change to standard output
    	print( "No more motion" )
    	previousMotionSensorState = False
    # Sleep for .3 seconds then do it all over again
    time.sleep(.3)