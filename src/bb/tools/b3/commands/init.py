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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import os

from command import Command

class Init(Command):
  """$ b3 init"""

  def setup_parser(self, parser, args):
    parser.set_usage("\n"
                     "  %prog init\n")
    parser.disable_interspersed_args()
    parser.epilog = "Initialize new BB application"

  def execute(self):
    if os.path.exists(".bbapp"):
      print "Application was already initialized"
      exit(0)
    print "Initialize application"
    os.mkdir(".bbapp")
