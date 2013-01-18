# http://www.bionicbunny.org/

__copyright__ = "Copyright (c) 2013 Sladeware LLC"

import os
import traceback

from command import Command
from bb.tools.b3 import buildfile

DEFAULT_TARGET = ":all"

class Build(Command):
  """This class represents build command:

  $ b3 build [target]
  """

  def __init__(self, root_dir, parser, argv):
    Command.__init__(self, root_dir, parser, argv)
    if not self.args:
      self.args = [DEFAULT_TARGET]
    self.rules = []
    addresses = []
    for spec in self.args[0:]:
      try:
        addresses.append(buildfile.get_address(root_dir, spec))
      except:
        self.error("Problem parsing spec %s: %s" %
                   (spec, traceback.format_exc()))
    for address in addresses:
      try:
        rule = buildfile.get_rule(address)
      except:
        self.error("Problem parsing BUILD rule %s: %s" %
                   (address, traceback.format_exc()))
      if not rule:
        self.error("Rule %s does not exist" % address)
      self.rules.append(rule)

  def setup_parser(self, parser, args):
    parser.set_usage("\n"
                     "  %prog build (options) [target] (build args)\n"
                     "  %prog build (options) [target]... -- (build args)")
    parser.disable_interspersed_args()
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
                      default=False, help="Don't output result of empty rules")
    parser.add_option("--list-rules", action="store_true", dest="list_rules",
                      default=False, help="List existed rules")
    parser.epilog = "Builds the specified rule(s). Currently any additional" \
        "arguments are passed straight through to the ant build" \
        "system."

  def execute(self):
    if self.options.list_rules:
      print "List supported rules:"
      for rule in self.rules:
        print "\t", rule.name
      return
    for rule in self.rules:
      rule.execute()
