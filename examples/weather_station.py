#!/usr/bin/env python

import random
from time import sleep

import allthingstalk as talk

import logging
logging.basicConfig()
# logging.getLogger('allthingstalk').setLevel(logging.DEBUG)


class WeatherStation(talk.Device):
    temperature = talk.NumberAsset(unit='°C')
    humidity = talk.NumberAsset(unit='%')
    pressure = talk.NumberAsset(unit='mbar')
    shutdown = talk.StringAsset(kind=talk.Asset.ACTUATOR)


client = talk.Client('DEVICE TOKEN')
weather = WeatherStation(client=client, id='DEVICE ID')


@WeatherStation.feed.temperature
def log_temperature(device, value, at):
    print('Temperature changed on %s at %s to %s!'
          % (device.id, at, value))


shutdown = False


@WeatherStation.command.shutdown
def on_shutdown(device, value, at):
    global shutdown
    print('Shutting down')
    shutdown = True


while not shutdown:
    weather.temperature = random.random() * 32
    weather.humidity = random.random() * 100
    weather.pressure = 900 + random.random() * 200
    sleep(2)
