# http://www.bionicbunny.org/

from bb.tools.b3.rules.library import Library

class CCLibrary(Library):

  properties = (("programming_language", "c"),)

  def __init__(self, target=None, name=None, srcs=[], deps=[], copts=[]):
    super(CCLibrary, self).__init__(target=target, name=name, srcs=srcs,
                                    deps=deps)
