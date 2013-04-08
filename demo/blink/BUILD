# -*- coding: utf-8; mode: python; -*-
#
# Copyright (c) 2013 Sladeware LLC

from blink import sensor

propeller_binary(target = "blink",
                 srcs = [sensor, "blink.c"])

propeller_load(name = "blink-load",
               binary = "blink",
               deps = [":blink"],
               terminal_mode = False,
               port = "/dev/ttyUSB0",
               eeprom = False)
