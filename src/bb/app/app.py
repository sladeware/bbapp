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

"""This module describes BB application."""

from __future__ import absolute_import

import inspect
import types
import os

from bb.utils import typecheck
from bb.utils import path_utils
from bb.app.imc_network import Network
from bb.app.mapping import Mapping

SETTINGS_DIR = ".bbapp"

class Application(object):
  """Base class for those who needs to maintain global application state.

  Normally you don't need to subclass this class.

  .. todo::

     Connect b3 build directory and application build directory.

  :param home_dir: represents root directory for the application.
  :param init_home_dir: if `home_dir` was specified and it's not existed home
         directory, the new directory will be initialized if `init_home_dir` is
         `True`.
  """

  _register = {}

  def __init__(self, home_dir=None, init_home_dir=False):
    self._network = Network()
    self._home_dir = None
    self._build_dir = None
    if home_dir:
      if not self.is_home_dir(home_dir) and init_home_dir:
        self.init_home_dir(home_dir)
      self.set_home_dir(home_dir)

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

  def __str__(self):
    return "%s[home_dir='%s',num_mappings=%d]" \
        % (self.__class__.__name__, self.get_home_dir(),
           self.get_num_mappings())

  @classmethod
  def get_active_instance(cls):
    """Returns active application instance. See also :func:`identify_instance`.

    :returns: An :class:`Application` instance.
    """
    return cls.identify_instance()

  @classmethod
  def identify_instance(cls, obj=None):
    """Identifies last active application instance.

    :param obj: Returns instance that keeps this object if such was provided.
    :returns: An :class:`Application` instance that represents active
      application.
    """
    src = obj and inspect.getsourcefile(obj) or None
    home_dir = src and cls.find_home_dir(src) or cls.identify_home_dir()
    if not cls._register.has_key(home_dir):
      return Application(home_dir=home_dir)
    return cls._register[home_dir]

  @classmethod
  def init_home_dir(cls, home_dir):
    """Initializes passed home directory if such wasn't already initialized.

    :returns: Path to home directory.
    """
    if not path_utils.exists(home_dir):
      raise IOError("'%s' doesn't exist" % home_dir)
    settings_dir = path_utils.join(home_dir, SETTINGS_DIR)
    path_utils.mkpath(settings_dir)
    return home_dir

  @classmethod
  def is_home_dir(cls, path):
    """Returns whether or not a given path is application home directory.

    :returns: `True` or `False`.
    :raises: :class:`TypeError`, :class:`IOError`
    """
    if not typecheck.is_string(path):
      raise TypeError("'path' has to be a string")
    elif not path_utils.exists(path):
      raise IOError("'%s' path doesn't exist" % path)
    return SETTINGS_DIR in os.listdir(path)

  @classmethod
  def find_home_dir(cls, path):
    """Finds top directory of an application by a given path and returns home
    path. Returns `None` if home direcotry cannot be identified.

    :param path: Path to directory.

    :returns: Path as string or `None`.
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
    """Set application home directory. There should be no other applications
    registered to this home directory.

    :param home_dir: A string that represents path to home directory. The path
       should exists.

    :raises: :class:`IOError`
    """
    if not path_utils.exists(home_dir):
      raise IOError("`%s' doesn't exist" % home_dir)
    if self._home_dir:
      self._unregister_instance(self)
    if home_dir in self._register:
      raise IOError("%s is already using this home dir: %s" %
                      (self._register[home_dir], home_dir))
    self._home_dir = home_dir
    self._register_instance(self)

  def get_home_dir(self):
    """Returns home directory.

    :returns: A string that represents path to home directory.
    """
    return self._home_dir

  def set_build_dir(self, path, make=False):
    """Sets path to the build directory. The build directory will be used to
    store temporary/autogenerated and compiled build-files.

    :param path: Build-directory name.
    :param make: Whether or not the path needs to be created.
    """
    if not path_utils.exists(path):
      if not make:
        raise IOError("`%s' doesn't exist" % path)
      path_utils.mkpath(path)
    self._build_dir = path

  def get_build_dir(self):
    """Returns build directory"""
    return self._build_dir

  def get_network(self):
    """Returns network that represents all the mappings and their relations
    within this application.
    """
    return self._network

  def gen_default_mapping_name(self, mapping):
    """Generates a name for a given mapping. This name will be unique within
    this application. This technique is used by the mapping itself for
    registration.

    :param mapping: A :class:`~bb.app.mapping.Mapping` instance.

    :returns: A string represented mapping's name.

    :raises: TypeError
    """
    if not isinstance(mapping, Mapping):
      raise TypeError()
    frmt = mapping.__class__.name_format
    return frmt % self.get_num_mappings()

  def get_mappings(self):
    """Returns list of mappings registered by this application.

    :returns: A list of :class:`Mapping` instances.
    """
    return self._network.get_nodes()

  def get_num_mappings(self):
    """Returns number of mappings controlled by this application."""
    return len(self.get_mappings())

  def has_mapping(self, mapping):
    if not isinstance(mapping, Mapping):
      raise TypeError("Mapping must be derived from bb.app.mapping.Mapping")
    return self._network.has_node(mapping)

  def add_mapping(self, mapping):
    """Registers a mapping and adds it to the application network.

    :param mapping: A :class:`Mapping` instance.

    :returns: Whether or not the mapping was added.
    """
    if self.has_mapping(mapping):
      return False
    self._network.add_node(mapping)
    return True

  def add_mappings(self, mappings):
    """Adds mappings. See also :func:`add_mapping`.

    :param mappings: A list of :class:`Mapping` instances.
    """
    if not typecheck.is_list(mappings):
      raise TypeError("'mappings' must be list")
    for mapping in mappings:
      self.add_mapping(mapping)

  def create_mapping(self, *args, **kwargs):
    """Mapping factory, creates and returns a new mapping connected to this
    application.

    .. note::

       Use :func:`create_mapping` to automatically create a mapping and connect
       it to the active application. Otherwise you will have to create mapping
       manually and then use :func:`add_mapping` in order to connect it to
       specific :class:`Application` instance.

    :param args: A list of arguments.
    :param kwargs: A dict of key-word arguments.

    :returns: A :class:`~bb.app.mapping.Mapping` instance.
    """
    fixed_kwargs = dict(**kwargs)
    fixed_kwargs.update(autoreg=False)
    mapping = Mapping(*args, **fixed_kwargs)
    self.add_mapping(mapping)
    return mapping

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

def create_application(*args, **kwargs):
  return Application(*args, **kwargs)

def delete_application(app):
  Application._unregister_instance(app)

def get_active_application():
  """Returns active application. See :func:`Application.get_active_instance` for
  details.

  :returns: An :class:`Application` instance.
  """
  return Application.get_active_instance()

def idenfity_application(obj=None):
  """Identifies active application or an application that manages a given
  object.

  :returns: An :class:`Application` instance.
  """
  return Application.identify_instance(obj)

def create_mapping(*args, **kwargs):
  """Creates a mapping.

  :returns: A :class:`~bb.app.mapping.Mapping` instance."""
  return Mapping(*args, **kwargs)
