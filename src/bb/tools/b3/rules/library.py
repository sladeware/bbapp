# -*- coding: utf-8; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko

from bb.tools.b3 import buildfile

class Library(buildfile.Primitive, buildfile.Rule, buildfile.Rule.WithSources):

  abstract = True

  def __init__(self, target=None, name=None, srcs=[], deps=[]):
    buildfile.Rule.__init__(self, target=target, name=name, deps=deps)
    buildfile.Rule.WithSources.__init__(self, srcs=srcs)
