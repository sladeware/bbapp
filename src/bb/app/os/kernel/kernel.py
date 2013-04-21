# http://www.bionicbunny.org/
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

"""A kernel is described by :class:`Kernel` and represents a non-blocking
computational resource, which is in most cases simply a core of a
microcontroller. Threads run within a kernel using a customizable time sharing
scheduler algorithm.
"""

from __future__ import print_function

from bb.utils import typecheck
from bb.app.os.port import Port
from bb.app.os.thread import Thread
from bb.app.os.kernel.schedulers import Scheduler, StaticScheduler

class Kernel(object):
  """The heart of BB operating system.

  :param core: A
    :class:`~bb.app.hardware.devices.processors.processor.Core` instance.
  :param threads: A list of :class:`~bb.app.os.thread.Thread` instances.
  :param scheduler: A :class:`~bb.app.os.kernel.schedulers.scheduler.Scheduler`
    instance.
  """

  def __init__(self, core=None, threads=[], scheduler=None):
    self._core = None
    self._ports = dict()
    self._threads = dict()
    # Select scheduler first if defined before any thread will be added
    # By default, if scheduler was not defined will be used static
    # scheduling policy.
    self._scheduler = None
    if threads:
      self.register_threads(threads)
    if scheduler:
      self.set_scheduler(scheduler)
    else:
      self._scheduler = StaticScheduler()
    if core:
      self.set_core(core)

  def __str__(self):
    return '%s[threads=%d, ports=%d]' % \
        (self.__class__.__name__, self.get_num_threads(), self.get_num_ports())

  def __build__(self):
    return self.get_threads()

  def set_core(self, core):
    """Selects the core on which this kernel will be executed.

    :param core: A :class:`~bb.app.hardware.devices.processors.processor.Core` instance.
    :raises: TypeError
    """
    self._core = core

  def get_core(self):
    """Returns core on which the kernel will be executed."""
    return self._core

  @property
  def core(self):
    return self.get_core()

  def set_scheduler(self, scheduler):
    """Selects scheduler that will manage threads.

    :param scheduler: A :class:`~bb.app.os.kernel.schedulers.scheduler.Scheduler` instance.
    :raises: TypeError
    """
    if not isinstance(scheduler, Scheduler):
      raise TypeError("Scheduler '%s' must be bb.os.kernel.Scheduler "
                      "sub-class" % scheduler)
    self._scheduler = scheduler

  def get_scheduler(self):
    """Returns used scheduler."""
    return self._scheduler

  def get_threads(self):
    return self._threads.values()

  def get_num_threads(self):
    return len(self.get_threads())

  def unregister_thread(self, thread):
    if not isinstance(thread, Thread):
      raise TypeError()
    if thread.get_name() in self._threads:
      del self._threads[thread.get_name()]
    return thread

  def register_thread(self, thread):
    """Registers a thread. Returns :class:`bb.os.kernel.kernel.Kernel` object
    for further work.
    """
    if not isinstance(thread, Thread):
      raise TypeError("Must be bb.os.thread.Thread")
    if thread.get_name() in self._threads:
      raise Exception("Thread '%s' was already registered." % thread.get_name())
    self._threads[thread.get_name()] = thread
    return self

  def register_threads(self, threads):
    if not typecheck.is_list(threads):
      raise TypeError("Must be list")
    for thread in threads:
      self.register_thread(thread)

  def register_ports(self, ports):
    if not typecheck.is_sequence(ports):
      raise TypeError("ports must be a sequence.")
    for port in ports:
      self.register_port(port)

  def register_port(self, port):
    if not isinstance(port, Port):
      raise TypeError()
    if port.get_name() in self._ports:
      raise Exception("Port '%s' was already registered." % port.get_name())
    self._ports[port.get_name()] = port
    return self

  def get_ports(self):
    return self._ports.values()

  def get_num_ports(self):
    return len(self.get_ports())
