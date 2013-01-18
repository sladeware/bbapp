# http://www.bionicbunny.org/

from bb.tools.b3.buildfile import Primitive, Rule

class Fileset(Primitive, Rule, Rule.WithSources):

  def __init__(self, target=None, name=None, srcs=[], deps=[]):
    Rule.__init__(self, target, name, deps=deps)
    Rule.WithSources.__init__(self, srcs=srcs)

  def execute(self):
    pass
