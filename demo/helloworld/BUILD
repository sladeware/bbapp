# -*- encoding: utf-8; mode: python; -*-
#
# Copyright (c) 2013 Sladeware LLC
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

fileset(name = "helloworld_files",
        srcs = ["helloworld.c"])

cc_binary(name = "helloworld",
          srcs = [":helloworld_files"])

propeller_binary(name = "helloworld-propeller",
                 srcs = [":helloworld_files"])

propeller_load(name = "helloworld-propeller-load",
               binary = "helloworld-propeller",
               port = "/dev/ttyUSB0",
               deps = [":helloworld-propeller"])
