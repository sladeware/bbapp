# http://www.bionicbunny.org/
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

from bb import app as bbapp
from bb.utils.testing import unittest

class ApplicationTest(unittest.TestCase):

  def setup(self):
    self._app = bbapp.create_application()

  def teardown(self):
    del self._app

  def test_mapping_registration(self):
    self.assert_equal(0, self._app.get_num_mappings(),
                      msg="Active application %s" % str(self._app))
    self._app.add_mappings([bbapp.create_mapping("M1"),
                            bbapp.create_mapping("M2")])
    self.assert_equal(2, self._app.get_num_mappings())
