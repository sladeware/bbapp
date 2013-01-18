# Copyright (c) 2012 Sladeware LLC

from django.conf import settings
import logging
import os

import bb
import bb.config.compilers.python.builtins
import bb.config.compilers.python.importer # override standard __import__

logger = logging.getLogger()
#logger.setLevel(1 * 10)
logging.basicConfig(level=logging.DEBUG,
                    format="[%(levelname).1s] %(message)s")
# NOTE: full-size format: %(levelname) 7s
logging.captureWarnings(True)

# We would like to use Django templates without the rest of Django.
settings.configure()
