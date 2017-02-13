#! /usr/bin/env python

import sys
import os
import extargsparse
import unittest

class debug_testmak_case(unittest.TestCase):
	def 



def main():
	commandline='''
	{
		"verbose|v" : "+",
		"failfast|f" : false,
		"$" : "*"
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	sys.argv[1:] = args.args
	unittext.main(verbosity=args.verbose,failfast=args.failfast)
	return

if __name__ == '__main__':
	main()
