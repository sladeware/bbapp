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

"""This module describes BB application. An application is defined by a BB model
and is comprised of a set of processes running on a particular system topology
to perform work meeting the application's requirements. Each process correnspond
to the appropriate :class:`bb.app.mapping.Mapping` instance from `mappings`.

For example, the following simple code snippet prints the current application
state:

    import bb.app
    print bb.app.get_active_application()
"""

import inspect
import types
import os

from bb.utils import typecheck
from bb.utils import path_utils
from .imc_network import Network
from .mapping import Mapping

__all__ = ["Application"]

SETTINGS_DIR = ".bbapp"

class Application(object):
  """Base class for those who needs to maintain global application state.

  Normally you don't need to subclass this class.

  `home_dir` represents root directory for the application. If `home_dir` was
  specified and it's not existed home directory, the new directory will be
  initialized if `init_home_dir` is `True`.
  """

  _register = {}

  def __init__(self, home_dir=None, init_home_dir=False):
    self._network = Network()
    self._home_dir = None
    self._build_dir = None
    home_dir = home_dir or os.getcwd()
    if not self.is_home_dir(home_dir) and init_home_dir:
      self.init_home_dir(home_dir)
    self.set_home_dir(home_dir)
    #default_build_dir = path_utils.join(self._home_dir, self.__class__.build_dir)
    #self.set_build_dir(default_build_dir, make=True)

  @classmethod
  def _register_instance(cls, app):
    if not isinstance(app, Application):
      raise TypeError("app must be derived from Application")
    if not app.get_home_dir() in cls._register:
      cls._register[app.get_home_dir()] = app

  @classmethod
  def _unregister_instance(cls, app):
    if not isinstance(app, Application):
      raise TypeError("app must be derived from Application")
    if app.get_home_dir() in cls._register:
      del cls._register[app.get_home_dir()]

  def __del__(self):
    self._unregister_instance(self)

  def __str__(self):
    return "%s[home_dir='%s',num_mappings=%d]" \
        % (self.__class__.__name__, self.get_home_dir(),
           self.get_num_mappings())

  #instance_mngmnt

  @classmethod
  def get_active_instance(cls):
    return cls.identify_instance()

  @classmethod
  def identify_instance(cls, obj=None):
    """Identifies or returns last active application instance. If `obj` was
    provided, returns instance that keeps this object. By default returns
    :class:`Application` instance that represents active application.
    """
    src = obj and inspect.getsourcefile(obj) or None
    home_dir = src and cls.find_home_dir(src) or cls.identify_home_dir()
    if not cls._register.has_key(home_dir):
      return Application(home_dir=home_dir)
    return cls._register[home_dir]

  #home_dir_mngmnt

  @classmethod
  def init_home_dir(cls, home_dir):
    """Initializes passed home directory if such wasn't already
    initialized. Returns path to home directory.
    """
    if not path_utils.exists(home_dir):
      raise IOError("'%s' doesn't exist" % home_dir)
    settings_dir = path_utils.join(home_dir, SETTINGS_DIR)
    path_utils.mkpath(settings_dir)
    return home_dir

  @classmethod
  def is_home_dir(cls, path):
    if not typecheck.is_string(path):
      raise TypeError("'path' has to be a string")
    elif not path_utils.exists(path):
      raise IOError("'%s' path doesn't exist" % path)
    return SETTINGS_DIR in os.listdir(path)

  @classmethod
  def find_home_dir(cls, path):
    """Finds top directory of an application by a given path and returns home
    path. Returns None if home direcotry cannot be identified.
    """
    if not typecheck.is_string(path):
      raise TypeError("'path' must be a string")
    elif not len(path):
      raise TypeError("'path' is empty")
    path = path_utils.realpath(path)
    if path_utils.isfile(path):
      (path, _) = path_utils.split(path)
    while path is not os.sep:
      if os.path.exists(path) and os.path.isdir(path):
        if cls.is_home_dir(path):
          return path
      (path, _) = path_utils.split(path)
    return None

  @classmethod
  def identify_home_dir(cls):
    for record in inspect.stack():
      (frame, filename, lineno, code_ctx, _, index) = record
      path = path_utils.dirname(path_utils.abspath(filename))
      home_dir = cls.find_home_dir(path)
      if home_dir:
        return home_dir
    return cls.find_home_dir(path_utils.realpath(os.curdir)) or os.getcwd()

  def set_home_dir(self, home_dir):
    if not path_utils.exists(home_dir):
      raise Exception("`%s' doesn't exist" % home_dir)
    if self._home_dir:
      self._unregister_instance(self)
    if home_dir in self._register:
      raise Exception("%s is already using this home dir: %s" %
                      (self._register[home_dir], home_dir))
    self._home_dir = home_dir
    self._register_instance(self)

  def get_home_dir(self):
    """Returns home directory"""
    return self._home_dir

  #build_dir

  def set_build_dir(self, path, make=False):
    """Sets path to the build directory. The build directory will be used to
    store temporary/autogenerated and compiled build-files.
    """
    if not path_utils.exists(path):
      if not make:
        raise Exception("`%s' doesn't exist" % path)
      path_utils.mkpath(path)
    self._build_dir = path

  def get_build_dir(self):
    """Returns build directory"""
    return self._build_dir

  def get_network(self):
    return self._network

  #mapping_mngmnt

  def gen_default_mapping_name(self, mapping):
    if not isinstance(mapping, Mapping):
      raise TypeError()
    frmt = mapping.__class__.name_format
    return frmt % self.get_num_mappings()

  def get_mappings(self):
    """Returns list of mappings registered by this application."""
    return self._network.get_nodes()

  def get_num_mappings(self):
    """Returns number of mappings controlled by this application."""
    return len(self.get_mappings())

  def has_mapping(self, mapping):
    if not isinstance(mapping, Mapping):
      raise TypeError("Mapping must be derived from bb.app.mapping.Mapping")
    return self._network.has_node(mapping)

  def add_mapping(self, mapping):
    """Registers a mapping and adds it to the application network. Returns
    whether or not the mapping was added.
    """
    if self.has_mapping(mapping):
      return False
    self._network.add_node(mapping)
    return True

  def add_mappings(self, mappings):
    """Adds mappings from list `mappings`. See :func:`add_mapping`."""
    if not typecheck.is_list(mappings):
      raise TypeError("'mappings' must be list")
    for mapping in mappings:
      self.add_mapping(mapping)

  def remove_mapping(self, mapping):
    if not isinstance(mapping, Mapping):
      raise TypeError("'mapping' must be derived from %s" % Mapping.__class__)
    if not self.has_mapping(mapping):
      return False
    self._network.remove_node(mapping)
    return True

  def remove_mappings(self):
    for mapping in self.get_mappings():
      self.remove_mapping(mapping)
