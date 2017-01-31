#! /usr/bin/env python

import extargsparse
import sys
import tempfile
import unittest
import random
import logging
import time
import os
import string
import subprocess
import shutil
import re
import filecmp


class CheckFiles(object):
	def __init__(self,crignore=True):
		self.right_only = []
		self.left_only = []
		self.left_diffs = []
		self.right_diffs = []
		self.__crignore = crignore
		return

	def check_file(self,leftdir,rightdir,leftfile,rightfile):
		if leftfile is not None:
			self.left_only.append(os.path.join(leftdir,leftfile))
		if rightfile is not None:
			self.right_only.append(os.path.join(rightdir,rightfile))
		return

	def check_file_same(self,leftfile,rightfile):
		llines = []
		with open(leftfile,'rb') as f:
			for l in f:
				llines.append(l)
		rlines = []
		with open(rightfile,'rb') as f:
			for l in f:
				rlines.append(l)

		if len(llines) != len(rlines):
			logging.warn('[%s] (%d) != [%s] (%d)'%(leftfile,len(llines),rightfile,len(rlines)))
			return False

		i = 0
		while i < len(llines):
			ll = llines[i]
			rl = rlines[i]
			if rl != ll:
				if not self.__crignore:
					diffcnt = 0
					while diffcnt < len(ll) or diffcnt < len(rl):
						if ll[diffcnt] != rl[diffcnt]:
							break
						diffcnt = diffcnt + 1
					s = '[%d]([%s]<>[%s]) at offset[%d] (0x%02x) <> (0x%02x)\n'%(i,leftfile,rightfile,diffcnt,ord(ll[diffcnt]),ord(rl[diffcnt]))
					s += 'from >>>>>>>>>>>>>>>>\n'
					s += '%s'%(ll)
					s += 'to <<<<<<<<<<<<<<<<<<<\n'
					s += '%s'%(rl)
					if self.__crignore:
						logging.warn('%s'%(s))
					else:
						logging.debug('%s'%(s))
					return False
				ll = ll.replace('\r','')
				rl = rl.replace('\r','')
				if ll != rl:
					diffcnt = 0
					while diffcnt < len(ll) or diffcnt < len(rl):
						if ll[diffcnt] != rl[diffcnt]:
							break
						diffcnt = diffcnt + 1
					s = '[%d]([%s]<>[%s]) at offset[%d] (0x%02x) <> (0x%02x)\n'%(i,leftfile,rightfile,diffcnt,ord(ll[diffcnt]),ord(rl[diffcnt]))
					s += 'from >>>>>>>>>>>>>>>>\n'
					s += '%s'%(ll)
					s += 'to <<<<<<<<<<<<<<<<<<<\n'
					s += '%s'%(rl)
					if self.__crignore:
						logging.warn('%s'%(s))
					else:
						logging.debug('%s'%(s))
					return False
			i = i + 1
		return True


	def diff_callback(self,leftdir,rightdir,file):
		lfile = os.path.join(leftdir,file)
		rfile = os.path.join(rightdir,file)
		if not self.check_file_same(lfile,rfile):
			self.left_diffs.append(os.path.join(leftdir,file))
			self.right_diffs.append(os.path.join(rightdir,file))
		return

def make_dir_safe(dname=None):
	if dname is not None:
		if not os.path.isdir(dname):
			try:
				os.makedirs(dname)
			except:
				pass
			if not os.path.isdir(dname):
				raise Exception('can not make [%s]'%(dname))

def make_tempdir(prefix=None):
	make_dir_safe(prefix)
	return tempfile.mkdtemp(dir=prefix)

def make_tempfile(prefix=None):
	make_dir_safe(prefix)
	fd,result = tempfile.mkstemp(dir=prefix)
	os.close(fd)
	return result

def __get_subdirs(abspath):
	sroot = os.path.abspath(abspath)
	for root,dirs,files in os.walk(sroot,topdown=True):
		if sroot == root:
			return dirs
	return []

def select_random_subdir(root):
	rpath = os.path.abspath(os.path.realpath(root))
	mostdown = random.randint(1,100)
	i = 0
	curdir = rpath
	subdirs = []
	for i in range(mostdown):
		subdirs = __get_subdirs(curdir)
		if len(subdirs) == 0:
			return curdir,os.path.relpath(curdir,rpath)
		else:
			curdir = os.path.realpath(os.path.join(curdir,random.choice(subdirs)))
	if len(subdirs)	== 0:
		return curdir,os.path.relpath(curdir,rpath)
	curdir = os.path.realpath(os.path.join(curdir,random.choice(subdirs)))
	return curdir,os.path.relpath(curdir,rpath)



class debug_testcp_case(unittest.TestCase):
	print_chars=''
	def setUp(self):
		return

	def tearDown(self):
		return

	@classmethod
	def setupClass(cls):
		return

	@classmethod
	def tearDownClass(cls):
		return

	def format_dc(self,dc,ctx=None):
		if ctx is not None:
			for f in dc.left_only:
				ctx.check_file(dc.left,dc.right,f,None)
			for f in dc.right_only:
				ctx.check_file(dc.left,dc.right,None,f)
		if ctx is not None:
			for f in dc.diff_files:
				ctx.diff_callback(dc.left,dc.right,f)
		if ctx is not None:
			for f in dc.funny_files:
				ctx.check_file(dc.left,dc.right,f,f)
		for cdc in dc.subdirs:		
			self.format_dc(dc.subdirs[cdc],ctx)
		return


	def dircompare(self,fromdir,todir,crignore=True):
		dc = filecmp.dircmp(fromdir,todir)
		cfs = CheckFiles(crignore)
		self.format_dc(dc,cfs)
		return cfs

	def get_random_chars(self,charnum,istext=True):
		s = ''
		for i in range(charnum):
			curnum = random.randint(0,255)
			curch = chr(curnum)
			if istext:
				while True:
					if curch in string.printable:
						break
					curch = chr(random.randint(0,255))
			s += curch
		return s

	def cpin_call(self,pwddir,curdir):
		olddir = os.getcwd()
		try:
			pwddir = os.path.abspath(pwddir)
			pwddir = os.path.realpath(pwddir)
			os.chdir(pwddir)
			curdir = os.path.abspath(curdir)
			curdir = os.path.realpath(curdir)
			if not curdir.startswith(pwddir) and curdir != pwddir:
				raise Exception('[%s] not valid for (%s)'%(curdir,pwddir))
			curdir = os.path.relpath(curdir,pwddir)
			logging.warn('pwd [%s] curdir[%s]'%(pwddir,curdir))
			while curdir.startswith('/'):
				curdir = curdir[1:]
			if len(curdir) == 0:
				curdir = '.'
			cpin = os.environ['CPIN_BIN']
			cmd = ['bash',cpin,curdir]
			logging.warn('cmd (%s)'%(cmd))
			subprocess.check_call(cmd)
		finally:
			os.chdir(olddir)
		return


	def __cpin_all(self):
		todir = os.environ['CP_TO_DIR']
		fromdir = os.environ['CP_SMB_DIR']
		fromdir = make_tempdir(fromdir)
		frombasename = os.path.basename(fromdir)
		fromdirgit = os.path.join(fromdir,'.git')
		todir = os.path.join(todir,frombasename)
		todir = os.path.abspath(todir)
		todirgit = os.path.join(todir,'.git')
		todirgit = os.path.abspath(todirgit)
		todir = os.path.abspath(todir)
		make_dir_safe(todirgit)
		make_dir_safe(todir)
		make_dir_safe(fromdir)
		make_dir_safe(fromdirgit)
		filenum = random.randint(20,100)
		crfromfiles = []
		crfromfiles = self.random_make_subs(fromdir,filenum)
		# now copy the file
		self.cpin_call(todir,'.')
		cfs = self.dircompare(fromdir,todir,False)
		self.assertEqual(cfs.left_only,[])
		self.assertEqual(cfs.right_only,[])
		self.assertEqual(len(cfs.left_diffs),len(cfs.right_diffs))
		if len(cfs.left_diffs) > 0:
			for i in range(len(cfs.left_diffs)):
				self.assertTrue( cfs.left_diffs[i] in crfromfiles )
				cmpfs = CheckFiles(True)
				retval = cmpfs.check_file_same(cfs.left_diffs[i],cfs.right_diffs[i])
				self.assertEqual(retval,True)
		shutil.rmtree(todir)
		shutil.rmtree(fromdir)
		return

	def test_cpin_all(self):
		if 'CP_MAX_CNT' in os.environ.keys():
			maxnum = int(os.environ['CP_MAX_CNT'])
		else:
			maxnum = random.randint(1,3)
		for i in range(maxnum):
			self.__cpin_all()
		return

	def random_make_subs(self,fromdir,filenum):
		crfromfiles = []
		curdir = fromdir
		for i in range(filenum):
			curnum = random.randint(0,20)
			if curnum == 0:
				curdir = os.path.abspath(os.path.join(curdir,'..'))
				if len(curdir) < len(fromdir):
					curdir = fromdir
				logging.debug('curdir [%s]'%(curdir))
			elif curnum == 1:
				curdir = make_tempdir(curdir)
				logging.debug('curdir [%s]'%(curdir))
			else:
				# this is make file
				curfile = make_tempfile(curdir)
				istext = False
				if random.randint(0,1):
					istext= True
				cons = self.get_random_chars(3000,istext)
				with open(curfile,'w+b') as f:
					f.write(cons)
				if istext:
					crfromfiles.append(curfile)
					logging.debug('[%s] ascii text'%(curfile))
				else:
					logging.debug('[%s] binary'%(curfile))
		return crfromfiles

	def __cpin_sub(self):
		todir = os.environ['CP_TO_DIR']
		fromdir = os.environ['CP_SMB_DIR']
		fromdir = make_tempdir(fromdir)
		frombasename = os.path.basename(fromdir)
		fromdirgit = os.path.join(fromdir,'.git')
		todir = os.path.join(todir,frombasename)
		todir = os.path.abspath(todir)
		todirgit = os.path.join(todir,'.git')
		todirgit = os.path.abspath(todirgit)
		todir = os.path.abspath(todir)
		make_dir_safe(todirgit)
		make_dir_safe(todir)
		make_dir_safe(fromdir)
		make_dir_safe(fromdirgit)
		filenum = random.randint(20,100)
		curdir = fromdir
		logging.warn('fromdir [%s] frombasename [%s] curdir[%s] filenum[%d]'%(fromdir,frombasename,curdir,filenum))
		crfromfiles = self.random_make_subs(fromdir,filenum)
		# now copy the file
		self.cpin_call(todir,'.')
		# now to make the 
		sdir,relpath = select_random_subdir(fromdir)
		crfromfiles = []
		filenum = random.randint(1,100)
		logging.warn('fromdir[%s] todir[%s] curdir[%s] filenum[%d]'%(fromdir,todir,curdir,filenum))
		crfromfiles = self.random_make_subs(sdir,filenum)

		self.cpin_call(todir,relpath)
		tosubdir = os.path.join(todir,relpath)
		fromsubdir = os.path.join(fromdir,relpath)
		cfs = self.dircompare(fromsubdir,tosubdir,False)
		self.assertEqual(cfs.left_only,[])
		self.assertEqual(cfs.right_only,[])
		self.assertEqual(len(cfs.left_diffs),len(cfs.right_diffs))
		if len(cfs.left_diffs) > 0:
			for i in range(len(cfs.left_diffs)):
				self.assertTrue( cfs.left_diffs[i] in crfromfiles )
				cmpfs = CheckFiles(True)
				retval = cmpfs.check_file_same(cfs.left_diffs[i],cfs.right_diffs[i])
				self.assertEqual(retval,True)
		shutil.rmtree(todir)
		shutil.rmtree(fromdir)
		return

	def test_cpin_sub(self):
		if 'CP_MAX_CNT' in os.environ.keys():
			maxnum = int(os.environ['CP_MAX_CNT'])
		else:
			maxnum = random.randint(1,3)
		for i in range(maxnum):
			self.__cpin_sub()
		return


def set_log_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    elif args.verbose >= 1 :
        loglvl = logging.WARN
    # we delete old handlers ,and set new handler
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return


def main():
	commandline_fmt='''
		{
			"verbose|v" : "+",
			"failfast|f" : false,
			"cpfromdir|F" : null,
			"cptodir|T" : null,
			"cpin|I" : "%s",
			"cpout|O" : "%s",
			"maxcnt|m" : 0,
			"$" : "*"
		}
	'''
	cpin = os.path.abspath(os.path.join(os.path.dirname(__file__),'cpin'))
	cpout = os.path.abspath(os.path.join(os.path.dirname(__file__),'cpout'))
	commandline=commandline_fmt%(cpin,cpout)
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	set_log_level(args)
	if args.cpfromdir is None:
		args.cpfromdir = make_tempdir('/tmp')	
	if args.cptodir is None:
		args.cptodir = make_tempdir('/tmp')
	args.cpfromdir = os.path.realpath(os.path.abspath(args.cpfromdir))
	args.cptodir = os.path.realpath(os.path.abspath(args.cptodir))
	if args.maxcnt != 0:
		os.environ['CP_MAX_CNT'] = '%d'%(args.maxcnt)
	else:
		if 'CP_MAX_CNT' in os.environ.keys():
			del os.environ['CP_MAX_CNT']
	os.environ['CP_SMB_DIR']= args.cpfromdir
	os.environ['CP_TO_DIR'] = args.cptodir
	os.environ['CPIN_BIN'] = args.cpin
	os.environ['CPOUT_BIN'] = args.cpout
	# to set the verbose mode
	os.environ['EXTARGS_VERBOSE'] = '%s'%(args.verbose)
	logging.warn('CP_TO_DIR [%s] CP_SMB_DIR [%s] '%(os.environ['CP_TO_DIR'],os.environ['CP_SMB_DIR']))
	random.seed(time.time())
	sys.argv[1:] = args.args
	unittest.main(verbosity=args.verbose,failfast=args.failfast)
	return

if __name__ == '__main__':
	main()
