# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC

__copyright__ = "Copyright (c) 2013 Sladeware LLC"

from bb.tools.b3.buildfile import Primitive, Rule

class Binary(Primitive, Rule, Rule.WithSources):

  def __init__(self, target=None, name=None, srcs=[], deps=[],
               compiler_class=None):
    Rule.__init__(self, target, name, deps=deps)
    Rule.WithSources.__init__(self, srcs=srcs)
    self.compiler = None
    if compiler_class:
      self.compiler = compiler_class()
