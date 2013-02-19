#!/usr/bin/env python
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
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
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

import optparse
import os
import sys
import unittest

import bb.config

TEST_FILE_SUFFIX = "*_test.py"
DEFAULT_VERBOSITY_LEVEL = 2

TOP_DIR = os.path.dirname(os.path.realpath(__file__))
SRC_DIR = os.path.join(TOP_DIR, "src")

def make_testsuite():
  """Returns test suite."""
  return unittest.TestLoader().discover(SRC_DIR, TEST_FILE_SUFFIX)

def run_tests():
  suite = make_testsuite()
  parser = optparse.OptionParser()
  parser.add_option("--verbosity-level",
                    type="int",
                    default=DEFAULT_VERBOSITY_LEVEL,
                    dest="verbosity_level",
                    help="set verbosity level to LEVEL",
                    metavar="LEVEL")
  (options, args) = parser.parse_args()
  unittest.TextTestRunner(verbosity=options.verbosity_level).run(suite)
  return 0

def main():
  try:
    run_tests()
  except Exception, e:
    return 1
  return 0

if __name__ == "__main__":
  sys.exit(main())
