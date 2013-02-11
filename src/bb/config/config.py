# -*- coding: utf-8; -*-
#
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

import django.conf
import logging
import os

import bb.config.compilers.python.builtins
import bb.config.compilers.python.importer # override standard __import__

logger = logging.getLogger()
# NOTE: full-size format: %(levelname) 7s
_LOG_FRMT = "[%(levelname).1s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=_LOG_FRMT)
logging.captureWarnings(True)

# We would like to use Django templates without the rest of Django.
django.conf.settings.configure()
