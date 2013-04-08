#!/usr/bin/env python
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC

from bb import app as bbapp
from bb.app import Mapping, Thread, Port
from bb.app.hardware.devices.boards import P8X32A_QuickStartBoard
from bb.app.meta_os.drivers.gpio import ButtonDriver

board = P8X32A_QuickStartBoard()
processor = board.get_processor()
sensor = bbapp.create_mapping(
  processor=processor,
  threads=[Thread("BLINKER", "blinker_runner", port=Port(10)),
           ButtonDriver("BUTTON_DRIVER", port=Port(10))]
)
