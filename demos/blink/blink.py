#!/usr/bin/env python

from bb.app import Application, Mapping, Thread
from bb.app.hardware.devices.processors import PropellerP8X32A_Q44
from bb.app.hardware.devices.boards import Protoboard
from bb.app.hardware.devices.leds import LED

processor = PropellerP8X32A_Q44()
led = LED()
board = Protoboard([processor, led])
blinker = Thread("BLINKER", "blinker_runner")
sensor = Mapping(processor=processor, threads=[blinker])
