#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import tempfile

from bb.testing import unittest
from bb.tools.compilers.propgcc import PropGCC

HELLO_WORLD_PROGRAM_MESSAGE = "Hello world!"
HELLO_WORLD_PROGRAM = """
#include <stdio.h>

int main()
{
  printf("%s");
  return 0;
}
""" % HELLO_WORLD_PROGRAM_MESSAGE

class PropGCCTest(unittest.TestCase):

  def test_compiling(self):
    input_fh = tempfile.NamedTemporaryFile(suffix=".c", delete=True)
    output_fh = tempfile.NamedTemporaryFile(suffix=".out", delete=False)
    compiler = PropGCC()
    compiler.set_output_file_path(output_fh.name)
    input_fh.write(HELLO_WORLD_PROGRAM)
    input_fh.seek(0)
    ok = True
    try:
      compiler.compile(sources=[input_fh.name])
    except Exception, e:
      ok = False
    input_fh.close()
    output_fh.close()
    self.assert_true(ok)

if __name__ == "__main__":
  unittest.main()
