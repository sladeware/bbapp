#!/usr/bin/env python
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
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

# http://peak.telecommunity.com/DevCenter/EasyInstall
from bootstrap import use_setuptools; use_setuptools()
# http://packages.python.org/distribute/setuptools.html
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import sys

sys.path = ["src/"] + sys.path
# Dynamically get the current version
version = __import__("bb").__version__

def touch():
  """This function should be called each time bb is installed."""
  import bb.config
  # NOTE: actually this call is redundant, since once bb.config is loaded it
  # will call read_user_settings() with will use gen_default_user_config() if
  # required.
  bb.config.gen_default_user_config()

class install(_install):

  def run(self):
    _install.run(self)
    touch()

class develop(_develop):

  def run(self):
    _develop.run(self)
    touch()

def main():
  setup(
    name = "bbapp",
    cmdclass = {
      "install": install,
      "develop": develop,
    },
    description = "BB Application Framework",
    version = version,
    author = "Bionic Bunny Team",
    author_email = "info@bionicbunny.org",
    url = "http://www.bionicbunny.org/",
    packages = find_packages("src"),
    package_dir = {'': 'src'},
    scripts = ["bin/b3"],
    license = "Apache",
    classifiers = [
      "License :: OSI Approved :: Apache Software License",
      "Development Status :: 2 - Pre-Alpha",
      "Operating System :: BBOS"
    ],
    install_requires = [
      "django",
      "distribute>=0.6.24",
      "networkx",
      "pyserial"
    ],
    test_suite = "test.make_testsuite",
  )

if __name__ == "__main__":
  main()
