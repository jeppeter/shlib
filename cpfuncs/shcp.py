#! /usr/bin/env python

import shutil
import sys
import os
import logging

def make_dir_safe(dname=None):
	if dname is not None:
		if not os.path.isdir(dname):
			try:
				logging.info('mkdir [%s]'%(dname))
				os.makedirs(dname)
			except:
				pass
			if not os.path.isdir(dname):
				raise Exception('can not make [%s]'%(dname))

def copy_dir(src,dst):
	make_dir_safe(dst)
	for root,dirs,files in os.walk(src):
		for c in dirs:
			nsrc = os.path.join(root,c)
			subpath = os.path.relpath(nsrc,src)
			ndst = os.path.join(dst,subpath)
			copy_dir(nsrc,ndst)
		for f in files:
			nsrc = os.path.join(root,f)
			subpath = os.path.relpath(nsrc,src)
			ndst = os.path.join(dst,subpath)
			logging.info('copy %s => %s'%(nsrc,ndst))
			shutil.copyfile(nsrc,ndst)
	return

def set_log_level(verbose):
    loglvl= logging.ERROR
    if verbose >= 3:
        loglvl = logging.DEBUG
    elif verbose >= 2:
        loglvl = logging.INFO
    elif verbose >= 1 :
        loglvl = logging.WARN
    # we delete old handlers ,and set new handler
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return

def main():
	if len(sys.argv[1:]) < 2:
		sys.stderr.write('%s from to'%(sys.argv[0]))
		sys.exit(3)
	if 'EXTARGS_VERBOSE' in os.environ.keys():
		logval = 0
		try:
			logval = int(os.environ['EXTARGS_VERBOSE'])
		except:
			logval = 0
		set_log_level(logval)
	src = os.path.realpath(sys.argv[1])
	dst = os.path.realpath(sys.argv[2])
	if os.path.isdir(src):
		if not os.path.isdir(dst):
			if os.path.exists(dst):
				raise Exception('%s not directory'%(dst))
			make_dir_safe(dst)
		copy_dir(src,dst)
	elif os.path.isfile(src):
		shutil.copyfile(src,dst)
	else:
		raise Exception('[%s] not valid file or directory'%(src))
	sys.exit(0)
	return

if __name__ == '__main__':
	main()