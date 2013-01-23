#!/usr/bin/env python
#
# Copyright (c) 2013 Sladeware LLC

import bb
from bb.app.hardware.devices.boards import P8X32A_QuickStartBoard
from bb.app.hardware.devices.leds import LED

board = P8X32A_QuickStartBoard()
processor = board.get_processor()
blinker = bb.app.Thread("BLINKER", "blinker_runner")
buttons = bb.app.Thread("BUTTONS", "buttons_runner")
sensor = bb.app.Mapping(processor=processor, threads=[blinker, buttons])
