# -*- coding: utf-8; -*-
#
# Copyright (c) 2012-2013 Sladeware LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Oleksandr Sviridenko

from __future__ import print_function

import sys

assert (2, 7) <= sys.version_info < (3, ), """\
This code is meant for Python
2.7 through 3.0. You might find that the parts you care about still work in
older Pythons or happen to work in newer ones, but you're on your own -- edit
__init__.py if you want to try it.
"""

from bb.config.config import *
from bb.config.user_config import *

try:
  user_settings = read_user_settings()
except Exception, e:
  print("Cannot read user settings:", e, file=sys.stderr)
  sys.exit(0)
