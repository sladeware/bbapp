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

from bb.utils.testing import unittest
from mapping import Mapping
from meta_os.thread import Thread

class MappingTest(unittest.TestCase):

  def test_thread_registration(self):
    t1 = Thread("T1")
    t2 = Thread("T2")
    mapping = Mapping("M1")
    mapping.register_threads([t1, t2])
    self.assert_equal(2, len(mapping.get_threads()))

  def test_name(self):
    mapping = Mapping("M1")
    self.assert_equal("M1", mapping.get_name())

if __name__ == "__main__":
  unittest.main()
