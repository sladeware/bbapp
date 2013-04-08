#!/usr/bin/env python
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

"""The messages are used by OS as the base unit for inter-thread
communication. A new message can be created with help of Message class as
follows:

  echo = Message('ECHO', ('text', 2))

The message echo here has ID 'ECHO' and one field 'text' of 2 bytes. Once a new
message has been created it can be registered by thread:

  thread = Thread('DEMO', 'demo_runner', messages=[echo])
  print thread.get_messages()

Once all the threads were registered within a mapping, all the messages that
will be available within an OS can be obtained with help of
Mapping.get_messages().
"""

from bb.utils import typecheck

class Field(object):
  """name - Name of this field, exactly as it appears in message
  struct/class."""

  def __init__(self, name, size=0):
    if not typecheck.is_string(name):
      raise TypeError('Field name has to be a string')
    self._name = name
    self._size = 0
    if size:
      self.size = size

  @property
  def name(self):
    return self._name

  @property
  def size(self):
    return self._size

  @size.setter
  def size(self, size):
    if not typecheck.is_int(size):
      raise TypeError("size must be int: %s" % size)
    self._size = size

class Message(object):
  """This class describes message structure passed between threads for
  communication purposes within OS. The message consists of ID represented by
  string and a set of fields, where each field described by class Field.
  """

  Field = Field

  def __init__(self, label, fields=[]):
    self._label = None
    self._fields = []
    if label:
      self.set_label(label)
    if fields:
      self.set_fields(fields)

  def get_byte_size(self):
    return sum([field.size for field in self.get_fields()])

  def get_label(self):
    return self._label

  def set_label(self, label):
    if not typecheck.is_string(label):
      raise TypeError('`label` has to be a string')
    self._label = label

  def get_fields(self):
    return self._fields

  def set_fields(self, fields):
    self._fields = []
    if not typecheck.is_list(fields) and not typecheck.is_tuple(fields):
      raise TypeError("`fields` has to be list or tuple: %s" % fields)
    for field in fields:
      if typecheck.is_list(field) or typecheck.is_tuple(field):
        field = self.Field(field[0], field[1])
      elif not isinstance(field, self.Field):
        field = self.Field(field)
      self._fields.append(field)

  def __str__(self):
    return '%s[label=%s, byte_size=%d, fields=(%s)]' % \
        (self.__class__.__name__, self.get_label(), self.get_byte_size(),
         ','.join([_.name for _ in self._fields]))
