# -*- coding: utf-8; -*-
#
# Copyright (c) 2012-2013 Sladeware LLC
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

from bb.app.meta_os import Driver, Message

class ButtonDriver(Driver):
  name_format = "BUTTON_DRIVER_%d"
  runner = "button_driver_runner"
  message_handlers = [
    ('is_button_pressed', ('IS_BUTTON_PRESSED', [('pin', 1)])),
    ('are_buttons_pressed', ('ARE_BUTTONS_PRESSED', [('mask', 4)])),
  ]
