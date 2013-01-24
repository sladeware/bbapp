# -*- coding: utf-8 -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

from bb.tools.b3 import buildfile
from bb.tools.b3.rules.binary import Binary
from bb.tools.b3.rules.fileset import Fileset
from bb.tools.compilers import GCC
from bb.utils import typecheck

class CCBinary(Binary):

  is_language_dependent = True
  properties = (("programming_language", "c"),)

  def __init__(self, target=None, name=None, srcs=[], deps=[],
               compiler_class=None):
    if not compiler_class:
      compiler_class = GCC
    Binary.__init__(self, target=target, name=name, srcs=srcs, deps=deps,
                    compiler_class=compiler_class)

  def execute(self):
    print("Build cc binary '%s' with '%s'" %
          (self.get_name(), self.compiler.__class__.__name__))
    buildfile.dependency_graph.resolve_forks()
    for src in self.get_sources():
      if typecheck.is_string(src):
        self.compiler.add_file(src)
      elif isinstance(src, Fileset):
        self.compiler.add_files(src.get_sources())
    if not self.compiler.get_files():
      print "No input files"
      exit(0)
    self.compiler.set_output_filename(self.get_name())
    self.compiler.compile()
