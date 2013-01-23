# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

try:
  import ConfigParser
except ImportError:
  import configparser as ConfigParser

import django.conf
import logging
import os

import bb.config.compilers.python.builtins
import bb.config.compilers.python.importer # override standard __import__

logger = logging.getLogger()
# NOTE: full-size format: %(levelname) 7s
_LOG_FRMT = "[%(levelname).1s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=_LOG_FRMT)
logging.captureWarnings(True)

# We would like to use Django templates without the rest of Django.
django.conf.settings.configure()

USER_CONFIG_FILENAME = ".bbconfig"

DEFAULT_USER_CONFIG = """
[bbos]
  location =

[b3]
  builddir = ~/.b3
"""

def set_user_config(cfg):
  pass

def touch_user_config(path):
  with open(path, "w") as fh:
    fh.write(DEFAULT_USER_CONFIG)

def get_user_config():
  path = os.path.expanduser("~/%s" % USER_CONFIG_FILENAME)
  if not os.path.exists(path):
    touch_user_config(path)
  return read_user_config(path)

def read_user_config(path):
  return UserConfig(path)

class UserConfig(ConfigParser.SafeConfigParser):
  """Encapsulates ini-style config file."""

  def __init__(self, path):
    ConfigParser.SafeConfigParser.__init__(self)
    with open(path) as config:
      self.readfp(config, filename=path)
    self._path = path

  get_sections = ConfigParser.SafeConfigParser.sections

  def write(self, fileobject=None):
    if not fileobject:
      with open(self._path, "w") as config:
        ConfigParser.SafeConfigParser.write(self, config)
    else:
      ConfigParser.SafeConfigParser.write(self, fileobject)

  def dump(self):
    print "Dump cofig", self._path
    for section in self.get_sections():
      print "[%s]" % section
      for name, value in self.items(section):
        print "%s = %s" % (name, value)
