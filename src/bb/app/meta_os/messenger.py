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

"""The messenger is ITC wrapper that hides message routing.

The following example shows the most simple case how to define a new message
handler by using :func:`Messenger.message_handler` decorator::

  serial_open_msg = Message('SERIAL_OPEN', ('rx', 'tx'))
  serial_messenger = Messenger('SERIAL_MESSENGER')
  serial_messenger.add_message_handler(
    MessageHandler('serial_open_handler', serial_open_msg))

Or the same example, but as a class::

  class SerialMessenger(Messenger):
    message_handlers = [
      ('serial_open_handler', ('SERIAL_OPEN', [('rx', 2), ('tx', 2)]))
    ]

When a :class:`SerialMessenger` object receives a ``SERIAL_OPEN`` message, the
message is directed to :func:`serial_open_handler` handler for the actual
processing.
"""

from bb.utils import logging
from bb.utils import typecheck
from thread import Thread
from bb.app.meta_os.message import Message

logger = logging.get_logger("bb")

class MessageHandler(object):

  def __init__(self, name, message, require_input=True, require_output=True):
    self._name = None
    self._set_name(name)
    self._message = message
    self._require_input = require_input
    self._require_output = require_output

  def __str__(self):
    return "%s[name='%s', message=%s]" % (self.__class__.__name__, self._name,
                                        self._message)

  def _set_name(self, name):
    if not typecheck.is_string(name):
      raise TypeError()
    self._name = name

  def get_name(self):
    return self._name

  def get_message(self):
    return self._message

  def is_input_required(self):
    return self._require_input

  def is_output_required(self):
    return self._require_output

class Messenger(Thread):
  """This class is a special form of thread, which allows to automatically
  provide an action for received message by using specified map of predefined
  handlers.

  .. note::

    In order to privent any conflicts with already defined methods the message
    handler should be named by concatinating `_handler` postfix to the the
    name of handler, e.g. ``serial_open_handler``.
  """

  message_handlers = []
  idle_action = None
  default_action = None

  def __init__(self, name=None, runner=None, message_handlers=[],
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

  def add_message_handler(self, handler):
    """Maps a command extracted from a message to the specified handler
    function. Note, handler's name should ends with '_handler'.
    """
    if not isinstance(handler, MessageHandler):
      raise TypeError('message handler has to be derived from MessageHandler')
    message = handler.get_message()
    if not self.register_message(message):
      return self
    if not handler.get_name().endswith('_handler'):
      logger.warning("Message handler %s that handles message %s "
                     "doesn't end with '_handler'"
                     % (handler.get_name(), message))
    self._message_handlers[message] = handler
    return self

  def add_message_handlers(self, message_handlers):
    """Add message handlers. message_handlers can be a list of
    MessageHandler's/tuples.
    """
    if not typecheck.is_list(message_handlers):
      raise TypeError('message_handlers has to be a list')
    for handler in message_handlers:
      if isinstance(handler, MessageHandler):
        self.add_message_handler(handler)
      else:
        if not typecheck.is_tuple(handler):
          raise TypeError("handler must be a tuple: %s" % type(handler))
        if len(handler) < 2:
          raise Exception("Handler should have more than two parameters")
        if typecheck.is_tuple(handler[1]):
          message = Message(*handler[1])
        else:
          raise TypeError()
        handler = list(handler)
        handler[1] = message
        handler = MessageHandler(*handler)
      self.add_message_handler(handler)
    return self
