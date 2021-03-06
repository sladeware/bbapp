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
# Author: Oleksandr Sviridenko

from bb.app import os
from bb.utils.testing import unittest

class ThreadTest(unittest.TestCase):

  def test_port(self):
    t0 = os.Thread("T0")
    self.assert_false(t0.has_port())
    t0.set_port(os.Port(10))
    self.assert_true(t0.has_port())
    t0.remove_port()
    self.assert_false(t0.has_port())

  def test_name(self):
    t0 = os.Thread("T0")
    self.assert_equal(t0.get_name(), "T0")

  def test_runner(self):
    t0 = os.Thread("T0", "old_hello_world")
    self.assert_equal(t0.get_runner(), "old_hello_world")
    t0.set_runner("new_hello_world")
    self.assert_equal(t0.get_runner(), "new_hello_world")
