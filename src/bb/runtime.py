# Copyright (c) 2012 Sladeware LLC
# http://www.bionicbunny.org/
#
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

"""This module represents BB runtime context and provides quick access to BB
state.

For example, the following simple code snippet prints the current application
state:

    import bb.runtime

    print bb.runtime.get_app()

"""

import inspect
import os
import sys

from bb.utils import path_utils
from bb.utils import typecheck

_base_app_class = None
_app_class = None
# Applications are registered by home directory
_apps = dict()

def set_app_class(cls):
  global _app_class
  if not issubclass(cls, _base_app_class):
    raise TypeError()
  _app_class = cls

def get_app_class():
  return _app_class

def find_app_dir(path):
  """Finds top directory of an application by a given path and returns home
  path.
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
      if _app_class.is_home_dir(path):
        return path
    (path, _) = path_utils.split(path)
  return None

def get_app_dir():
  for record in inspect.stack():
    (frame, filename, lineno, code_ctx, _, index) = record
    path = path_utils.dirname(path_utils.abspath(filename))
    home_dir = find_app_dir(path)
    if home_dir:
      return home_dir
  return find_app_dir(path_utils.realpath(os.curdir))

def identify_app(obj=None):
  """Identifies and returns last active application instance. If `obj` was
  provided, returns instance that keeps this object. By default returns
  :class:`Application` instance that represents active application.
  """
  src = obj and inspect.getsourcefile(obj) or None
  home_dir = src and find_app_dir(src) or get_app_dir()
  return _apps.setdefault(home_dir, _app_class(home_dir=home_dir))

def identify_app_or_die(*args, **kwargs):
  """Throws exception if instance cannot be defined. See
  :func:`identify_app`.
  """
  app = identify_app(*args, **kwargs)
  if not app:
    raise NotImplementedError()
  return app

def init():
  global _base_app_class
  if "bb.app.app" not in sys.modules:
    raise Exception()
  _base_app_class = sys.modules["bb.app.app"].Application
  set_app_class(_base_app_class)
  _apps[None] = _app_class()

get_app = get_active_app = identify_app
get_app_or_die = get_active_app_or_die = identify_app_or_die
get_active_apps = None
