# -*- coding: utf-8; -*-
#
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
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

"""The mapping of hardware resources to software runtime components such as
processes, threads, queues and pools is determined at compile time. Thereby
permitting system integrators to cleanly separate the concept of what the
software does and where it does it. This mapping is represented by class
:class:`bb.app.mapping.Mapping`.

Compile time mapping is critical for tuning a system based on application
requirements. It is useful when faced with an existing software application that
must run on a new or updated hardware platform, thus requiring re-tuning of the
application. Equally important is the flexibility afforded by compile time
mapping to system integrators that need to incorporate new software features as
applications inevitably grow in complexity.
"""

from bb.app.meta_os import OS, Thread, Port
from bb.app.hardware.devices.processors import Processor
from bb.utils import typecheck
from bb.utils import logging

logger = logging.get_logger("bb")

class ThreadDistributor(object):
  """Base class for thread distributors."""

  def distribute(self, threads, processor):
    raise NotImplementedError()

  def __call__(self, threads, processor):
    return self.distribute(threads, processor)

class RoundrobinThreadDistributor(ThreadDistributor):
  """Default thread distributor provides round-robin distribution of threads
  between all cores within the processors.
  """

  def distribute(self, threads, processor):
    """Distributes `threads` over `processor`'s cores."""
    distribution = {}
    for core in processor.get_cores():
      distribution[core] = []
    c = 0
    for thread in threads:
      if not isinstance(thread, Thread):
        raise TypeError("thread must be derived from Thread")
      core = processor.get_cores()[c]
      c = (c + 1) % len(processor.get_cores())
      distribution[core].append(thread)
    return distribution

class Mapping(object):
  """The mapping of hardware resources to software runtime components such as
  processes, threads, queues and pools is determined at compile time.

  .. note::
  On this moment device drivers for controlled devices will not be
  added automatically as threads. They should be added manually.
  """

  processor = None
  os_class = OS
  name_format = "M%d"

  def __init__(self, name=None, processor=None, os_class=None, threads=[],
               thread_distributor=None, autoreg=True):
    self._name = None
    self._threads = dict()
    self._ports = dict()
    self._os_class = None
    self._max_message_size = 0
    self._is_simulation_mode = False
    self._processor = None
    self._thread_distributor = None
    if not thread_distributor:
      thread_distributor = RoundrobinThreadDistributor()
    self.set_thread_distributor(thread_distributor)
    if name:
      self.set_name(name)
    if os_class or getattr(self.__class__, "os_class", None):
      self.set_os_class(os_class or self.__class__.os_class)
    if processor or self.__class__.processor:
      self.set_processor(processor or self.__class__.processor)
    if threads:
      self.register_threads(threads)
    if autoreg:
      self._register()

  def _register(self):
    import bb.app
    app = bb.app.get_active_application()
    if not self.get_name():
      self.set_name(app.gen_default_mapping_name(self))
    app.add_mapping(self)

  def __str__(self):
    return '%s[name=%s,processor=%s,thread_distributor=%s,is_simulation_mode=%s]' \
        % (self.__class__.__name__,
           self._name,
           self._processor and self._processor.__class__.__name__ or None,
           self._thread_distributor and \
             self._thread_distributor.__class__.__name__ or None,
           self._is_simulation_mode)

  def __build__(self):
    return self.gen_os()

  def __call__(self, *args, **kwargs):
    """The mapping instance call eq to gen_os()."""
    return self.gen_os(*args, **kwargs)

  def set_max_message_size(self, size):
    self._max_message_size = size

  def get_max_message_size(self):
    """Returns max message payload size in bytes."""
    return self._max_message_size

  def set_name(self, name):
    if not typecheck.is_string(name):
      raise TypeError("name must be string")
    self._name = name

  def get_name(self):
    return self._name

  #threads

  def set_thread_distributor(self, distributor):
    """Sets thread-distributor that will be used in OS generation process."""
    if not isinstance(distributor, ThreadDistributor):
      raise TypeError("Distributor must be derived from ThreadDistributor.")
    self._thread_distributor = distributor

  def get_thread_distributor(self):
    return self._thread_distributor

  def register_thread(self, thread, name=None):
    """Registers thread by its name. The name has to be unique within this
    mapping. If thread doesn't have a name and it wasn't provided, mapping will
    try to use its name format (see :func:`Thread.get_name_format`) to generate
    one.

    If the thread has a port, this port will be registered with threads name.
    """
    if not isinstance(thread, Thread):
      raise TypeError("Must be derived from bb.app.meta_os.Thread: %s", thread)
    if name and not typecheck.is_string(name):
      raise TypeError()
    if name:
      thread.set_name(name)
    else:
      if thread.get_name() is None:
        frmt = thread.get_name_format()
        if not frmt:
          logger.warning("Thread %s doesn't have a name and the format cannot"
                         "be obtained to generate one." % thread)
          return
        # TODO(team): improve name generation within a mapping; it has to be
        # unique.
        thread.set_name(frmt % self.get_num_threads())
      name = thread.get_name()
    if thread.has_port():
      self.register_port(thread.get_port(), name)
    self._threads[name] = thread

  def get_thread(self, name):
    if not typecheck.is_string(name):
      raise TypeError("'name' must be a string")
    return self._threads.get(name, None)

  def register_threads(self, threads):
    for thread in threads:
      self.register_thread(thread)

  def get_num_threads(self):
    """Returns number of thread within this mapping."""
    return len(self.get_threads())

  def get_threads(self):
    """Returns complete list of threads handled by this mapping."""
    return self._threads.values()

  def set_simulation_mode(self):
    self._is_simulation_mode = True

  def is_simulation_mode(self):
    return self._is_simulation_mode

  def get_processor(self):
    """Returns :class:`bb.app.hardware.devices.processors.processor.Processor`
    instance.
    """
    return self._processor

  def set_processor(self, processor):
    """Sets processor. The driver that controles this device will be added
    automatically.
    """
    if not isinstance(processor, Processor):
      raise TypeError("'processor' has to be derived from Processor class.")
    self._processor = processor
    driver = processor.get_driver()
    if not driver:
      logger.warning("Processor %s doesn't have a driver" % processor)
      return
    self.register_thread(driver)

  def is_processor_defined(self):
    """Returns whether or not a processor was defined. Returns ``True`` if the
    :class:`bb.hardware.devices.processors.processor.Processor` instance was
    defined, or ``False`` otherwise.
    """
    return not not self.get_processor()

  def set_os_class(self, os_class):
    """Sets OS class that will be used by :func:`gen_os` to generate OS
    instance.
    """
    if not issubclass(os_class, OS):
      raise TypeError("Must be derived from bb.app.meta_os.OS class: %s"
                      % os_class)
    self._os_class = os_class

  def get_os_class(self):
    return self._os_class

  def gen_os(self):
    """Generates OS based on mapping analysis. Returns
    :class:`bb.app.meta_os.meta_os.OS` based instance.
    """
    logger.info("Process mapping %s" % self.get_name())
    processor = self.get_processor()
    if not processor:
      raise Exception("Processor wasn't defined")
    if not self.get_num_threads():
      raise Exception("Mapping doesn't have threads. Nothing to do.")
    distributor = self.get_thread_distributor()
    if not distributor:
      raise Exception("Thread-distributor wasn't defined")
    logger.info("Generate OS")
    distribution = distributor(self.get_threads(), processor)
    for core, threads in distribution.items():
      if not threads:
        continue
      kernel_class = self._os_class.kernel_class
      kernel = kernel_class(core=core, threads=threads)
      core.set_kernel(kernel)
    os = self._os_class(processor=processor,
                        max_message_size=self.get_max_message_size())
    # A few simple verifications
    if not os.get_num_kernels():
      raise Exception("OS should have atleast one kernel.")
    processor.set_os(os)
    return os

  #ports

  def register_port(self, port, name):
    if not typecheck.is_string(name):
      raise TypeError("name must be a string")
    if not isinstance(port, Port):
      raise TypeError("port must be derived from Port")
    self._ports[name] = port

  def get_ports(self):
    return self._ports.values()
