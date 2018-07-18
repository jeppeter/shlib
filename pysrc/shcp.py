#! /usr/bin/env python

import shutil
import sys
import os
import logging
import re
import stat

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

def copy_dir(src,dst,based,copied=[],isexcept=False):
	make_dir_safe(dst)
	logging.info('src %s => dst %s'%(src,dst))
	totalerror = 0	
	for root,dirs,files in os.walk(src):
		for c in dirs:
			if c not in copied:
				nsrc = os.path.join(root,c)
				if os.path.islink(nsrc) or not (os.path.isdir(nsrc)):
					logging.warning('%s not valid file or directory'%(nsrc))
					continue
				subpath = os.path.relpath(nsrc,src)
				ndst = os.path.join(dst,subpath)
				make_dir_safe(ndst)
				copied.append(nsrc)
				#curerr = copy_dir(nsrc,ndst,based,copied,isexcept)
				#if curerr != 0 :
				#	totalerror = curerr
		for f in files:
			if f not in copied:
				nsrc = os.path.abspath(os.path.join(root,f))
				if not(os.path.isfile(nsrc) or os.path.isdir(nsrc)):
					logging.warning('%s not valid file or directory'%(nsrc))
					continue
				subpath = os.path.relpath(nsrc,src)
				ndst = os.path.join(dst,subpath)
				logging.info('copy %s => %s'%(nsrc,ndst))
				copied.append(nsrc)
				if isexcept:
					shutil.copyfile(nsrc,ndst)
				else:
					try:
						shutil.copyfile(nsrc,ndst)
					except:
						c = nsrc.replace(based,'',1)
						if c.startswith('%s'%(os.sep)):
							c = c.replace(os.sep,'',1)
						sys.stderr.write('%s error\n'%(c))
						if totalerror == 0:
							totalerror = 3
	return totalerror

def set_log_level(verbose):
    loglvl= logging.ERROR
    if verbose >= 3:
        loglvl = logging.DEBUG
    elif verbose >= 2:
        loglvl = logging.INFO
    elif verbose >= 1 :
        loglvl = logging.WARN
    # we delete old handlers ,and set new handler
    if hasattr(logging, 'root') and hasattr(logging.root, 'handlers') and len(logging.root.handlers) > 0:
    	logging.root.handlers = []
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return

def main():
	based = ''
	if len(sys.argv[1:]) < 2:
		sys.stderr.write('%s from to\n'%(sys.argv[0]))
		sys.exit(3)
	if len(sys.argv[1:]) >= 3:
		based = os.path.realpath(sys.argv[3])
	if 'EXTARGS_VERBOSE' in os.environ.keys():
		logval = 0
		try:
			logval = int(os.environ['EXTARGS_VERBOSE'])
		except:
			logval = 0
		set_log_level(logval)	
	src = os.path.realpath(sys.argv[1])
	dst = os.path.realpath(sys.argv[2])
	if len(based) == 0:
		based = src
	dstd = os.path.dirname(dst)
	err = 0
	if os.path.isdir(src):
		if not os.path.isdir(dst):
			if os.path.exists(dst):
				raise Exception('%s not directory'%(dst))
			make_dir_safe(dst)
		err = copy_dir(src,dst,based)
	elif os.path.isfile(src):
		if not os.path.exists(dstd):
			make_dir_safe(dstd)
		shutil.copyfile(src,dst)
	else:
		raise Exception('[%s] not valid file or directory'%(src))
	sys.exit(err)
	return

if __name__ == '__main__':
	main()