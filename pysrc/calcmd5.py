#! /usr/bin/env python

import extargsparse
import hashlib
import logging
import sys

def calc_md5(infile=None):
	md5 = hashlib.md5()
	fin = sys.stdin
	if infile is not None:
		fin = open(infile,'rb')
	while True:	
		if fin != sys.stdin:
			l = fin.read(1024)
		else:
			l = fin.buffer.read()
		if len(l) == 0:
			break
		md5.update(l)
	if fin != sys.stdin:
		fin.close()
	fin = None
	return md5.hexdigest()

def main():
	commandline='''
	{
		"verbose|v" : "+",
		"$" : "*"
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	if len(args.args) > 0:
		for c in args.args:
			s = calc_md5(c)
			print('%s %s'%(s,c))
	else:
		s = calc_md5()
		print('%s (stdin)'%(s))
	return

if __name__ == '__main__':
	main()