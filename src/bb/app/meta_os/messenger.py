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

"""The following example shows the most simple case how to define a new message
handler by using :func:`Messenger.message_handler` decorator::

  serial_open_msg = Message('SERIAL_OPEN', ('rx', 'tx'))
  serial_messenger = Messenger('SERIAL_MESSENGER')
  serial_messenger.add_message_handler(serial_open_msg, 'serial_open_handler')

Or the same example, but as a class::

  class SerialMessenger(Messenger):
    name = 'SERIAL_MESSENGER'
    message_handlers = {
      Message('SERIAL_OPEN', (('rx', 2), ('tx', 2))): 'serial_open_handler',
    }

When a :class:`SerialMessenger` object receives a ``SERIAL_OPEN`` message,
the message is directed to :func:`SerialMessenger.serial_open_handler`
handler for the actual processing.
"""

from bb.utils import logging
from bb.utils import typecheck
from thread import Thread
from message import Message

logger = logging.get_logger("bb")

class Messenger(Thread):
  """This class is a special form of thread, which allows to automatically
  provide an action for received message by using specified map of predefined
  handlers.

  .. note::

    In order to privent any conflicts with already defined methods the message
    handler should be named by concatinating `_handler` postfix to the the
    name of handler, e.g. ``serial_open_handler``.
  """

  message_handlers = {}
  idle_action = None
  default_action = None

  def __init__(self, name=None, runner=None, message_handlers={},
               idle_action=None, default_action=None, port=None):
    Thread.__init__(self, name, runner=runner, port=port)
    self._default_action = None
    self._idle_action = None
    self._message_handlers = {}
    if default_action or getattr(self.__class__, "default_action", None):
      self.set_default_action(default_action or self.__class__.default_action)
    if idle_action or getattr(self.__class__, "idle_action", None):
      self.set_idle_action(idle_action or self.__class__.idle_action)
    if message_handlers or getattr(self.__class__, "message_handlers", None):
      self.add_message_handlers(message_handlers \
                                  or self.__class__.message_handlers)

  def get_default_action(self):
    return self._default_action

  def set_default_action(self, action):
    if not typecheck.is_function(action):
      raise TypeError("action has to be a function: %s" % action)
    self._default_action = action

  def get_idle_action(self):
    return self._idle_action

  def set_idle_action(self, action):
    if not typecheck.is_function(action):
      raise TypeError("action has to be a function: %s" % action)
    self._idle_action = action

  def get_message_handler(self, message):
    if not isinstance(message, Message):
      raise TypeError('message has to be derived from Message')
    return self._message_handlers.get(message, None)

  def get_message_handlers(self):
    return self._message_handlers

  def add_message_handler(self, message, handler):
    """Maps a command extracted from a message to the specified handler
    function. Note, handler's name should ends with '_handler'.
    """
    if not self.register_message(message):
      return self
    if not typecheck.is_string(handler):
      raise TypeError('message handler has to be a string')
    if not handler.endswith('_handler'):
      logger.warning("Message handler '%s' that handles message '%s' "
                     "doesn't end with '_handler'" % (handler, message))
    self._message_handlers[message] = handler
    return self

  def add_message_handlers(self, message_handlers):
    if not typecheck.is_dict(message_handlers):
      raise TypeError('message_handlers has to be a dict')
    for message, handler in message_handlers.items():
      self.add_message_handler(message, handler)
    return self
