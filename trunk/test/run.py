# -*- coding: utf-8 -*-
#
# Copyright 2005 Fundación Via Libre
#
# This file is part of PAPO.
#
# PAPO is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# PAPO is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PAPO; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307 USA

import os, sys, re
import unittest
from optparse import OptionParser
import libxml2
libxml2.debugMemory(1)

# one per line so its more svn friendly
# (less conflicts)
moduleNames= ['testTransaction',
              'testStockAdjustment',
              'testReceipt', 
              'testCurrency',
              'testPrinter',
              'testPointOfSale',
              ]

parser = OptionParser()
parser.add_option('-v', '--verbose', help="be verbose",
                  action="store_true", default=False)
parser.add_option('-q', '--quiet', help="be quiet",
                  action="store_true", default=False)
parser.add_option('-s', '--sync', help="make X calls synchronous",
                  action="store_true", default=False)
parser.add_option('-M', '--module', action="append",
                  help="test this module (may be specified multiple times)")

test_options, args = parser.parse_args()

argv = sys.argv[:1]
if test_options.verbose:
    argv.append('-v')
if test_options.quiet:
    argv.append('-q')

if test_options.module:
    moduleNames = test_options.module

import run
run.test_options = test_options

for i in moduleNames:
    exec 'from %s import *' % i

if __name__ == '__main__':
    print >> sys.stderr, "All tests loaded Ok."
    unittest.main(argv=argv)

    #libxml2.cleanupParser()
    if libxml2.debugMemory(1) == 0:
        print "OK"
    else:
        print "Memory leak %d bytes" % (libxml2.debugMemory(1))
        libxml2.dumpMemory()
