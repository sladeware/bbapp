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
# Author: Oleksandr Sviridenko

"""Contains high-level classes encapsulating the overall BB application
model.

BB application combines all of the build systems of all of the defined
processes. Therefore the application includes the models of processes, their
communication, hardware description, simulation and build specifications. At the
same time the processes inside of an application can be segmented into
`clusters`, or a group of CPUs.
"""

from app import *
from mapping import Mapping, Thread, Port, mapping_class_factory

def create_application(*args, **kwargs):
  return Application(*args, **kwargs)

def delete_application(app):
  Application._unregister_instance(app)

def get_active_application():
  return Application.get_active_instance()

def idenfity_application(obj=None):
  return Application.identify_instance(obj)

def create_mapping(*args, **kwargs):
  return Mapping(*args, **kwargs)
