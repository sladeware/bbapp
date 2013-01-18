#!/usr/bin/env python
#
# http://www.bionicbunny.org/
# Copyright (c) 2012 Sladeware LLC
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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import logging

import bb
from bb.app import Mapping
from bb.tools import b3
from bb.utils import path as path_utils
from bb import host_os

class MappingBuildAgent:
  """This build-agent aims to help build Mapping derived instances."""

  def on_build_start(self, builder):
    builder.set_build_dir([bb.runtime.get_app().get_build_dir(),
                           self.object.get_name()])

  def on_assemble(self, builder, image):
    mapping = self.object
    if not isinstance(mapping, Mapping):
      raise TypeError()
    logging.info("Processing mapping '%s'..." % mapping.get_name())
    if not mapping.get_num_threads():
      logging.critical("Mapping", mapping.get_name(), "doesn't have threads.")
      return
    logging.info("Generating OS")
    os = mapping.gen_os()
    if not isinstance(os, mapping.META_OS_CLASS):
      raise TypeError("The 'os' has to be derived from MetaOS class.")
    logging.info("processor: %s" % os.get_processor())
    logging.info("num messages: %d" % len(os.get_messages()))
    logging.info("messages:")
    for i, message in enumerate(os.get_messages()):
      logging.info(" %d. %s" % (i, message))
    logging.info("max message size: %s byte(s)" % os.get_max_message_size())
    image.add_object(os)
    if not os.get_num_kernels():
      raise Exception("OS should have atleast one kernel.")
    for i, kernel in enumerate(os.get_kernels()):
      image.add_object(kernel)
      logging.info("Processing kernel#%d..." % i)
      image.add_object(kernel.get_scheduler())
      logging.info("num threads: %s" % kernel.get_num_threads())
      logging.info("threads:")
      for i, thread in enumerate(kernel.get_threads()):
        logging.info(" %d. %s" % (i, thread))
        image.add_object(thread)
    # TODO(team): when to add processor object?
    image.add_object(os.get_processor())
