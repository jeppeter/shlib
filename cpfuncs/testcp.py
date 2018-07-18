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


namechars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

class CheckFiles(object):
	def __init__(self,crignore=True):
		self.only = []
		self.diffs = []
		self.crignore = crignore
		return

	def check_file_same(self,leftfile,rightfile):
		llines = []
		logging.info('leftfile [%s] rightfile [%s]'%(leftfile,rightfile))
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
				if not self.crignore:
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
					if self.crignore:
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
					if self.crignore:
						logging.warn('%s'%(s))
					else:
						logging.debug('%s'%(s))
					return False
			i = i + 1
		return True


	def __format(self):
		s = ''
		s += 'only %s diffs %s'%(self.only, self.diffs)
		return s

	def __str__(self):
		return self.__format()

	def __repr__(self):
		return self.__format()


class CompoundCheckFiles(CheckFiles):
	def __init__(self,crignore=True):
		super(CompoundCheckFiles,self).__init__(crignore)
		self.left_diffs = []
		self.right_diffs = []
		self.left_only = []
		self.right_only = []
		return

	def __format(self):
		s = ''
		s += 'left_only [%d] [%s]\n'%(len(self.left_only),self.left_only)
		s += 'left_diffs [%d] [%s]\n'%(len(self.left_diffs),self.left_diffs)
		s += 'right_only [%d] [%s]\n'%(len(self.right_only),self.right_only)
		s += 'right_diffs [%d] [%s]\n'%(len(self.right_diffs),self.right_diffs)
		return s

	def __str__(self):
		return self.__format()

	def __repr__(self):
		return self.__format()

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

def make_templink(dirn=None, tolink='.'):
	make_dir_safe(dirn)
	abdir = os.path.abspath(dirn)
	existed = True
	while existed:
		existed = False
		nchars = random.randint(12, 30)
		cname = ''
		for i in range(nchars):
			cname += random.choice(namechars)
		nlink = os.path.join(abdir,cname)
		if os.path.exists(nlink):
			existed = True
		else:
			os.symlink(tolink,nlink)
	return nlink

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

	def __compare_dir(self,fromdir,todir,crignore=True):
		cfs = CheckFiles(crignore)
		for root, dirs,files in os.walk(fromdir):
			if root == fromdir  or root == os.path.join(fromdir,os.pathsep):
				npart = ''
			else:
				npart = os.path.relpath(root,fromdir)
			logging.info('npart %s root %s'%(npart, root))
			for d in dirs:
				nd = os.path.join(npart,d)
				nfdir = os.path.join(root,d)
				ntdir = os.path.join(todir,npart,d)
				if not os.path.exists(ntdir):					
					if nd not in cfs.only:
						cfs.only.append(nd)
					continue
			for f in files:
				nf = os.path.join(npart,f)
				nffile = os.path.join(root,f)
				ntfile = os.path.join(todir,npart,f)
				if not os.path.exists(ntfile):
					if nf not in cfs.only:
						cfs.only.append(nf)
					continue
				# now we should check whether
				if (os.path.islink(ntfile) and not (os.path.islink(nffile))) or (not os.path.islink(ntfile) and (os.path.islink(nffile))):
					if nf not in cfs.diffs:
						cfs.diffs.append(nf)
					continue

				retval = cfs.check_file_same(nffile,ntfile)	
				if not retval:
					if nf not in cfs.diffs:
						cfs.diffs.append(nf)
		return cfs

	def dircompare(self,fromdir,todir,crignore=True):
		compound = CompoundCheckFiles(crignore)
		cfs = self.__compare_dir(fromdir, todir,crignore)
		for d in cfs.diffs:
			nd = os.path.join(fromdir,d)
			if nd not in compound.left_diffs:
				logging.debug('left_diffs append [%s]'%(nd))
				compound.left_diffs.append(nd)
		for d in cfs.only:
			nd = os.path.join(fromdir,d)
			if nd not in compound.left_only:
				logging.debug('left_only append [%s]'%(nd))
				compound.left_only.append(nd)

		cfs = self.__compare_dir(todir,fromdir,crignore)
		for d in cfs.diffs:
			nd = os.path.join(todir,d)
			if nd not in compound.right_diffs:
				logging.debug('right_diffs append [%s]'%(nd))
				compound.right_diffs.append(nd)
		for d in cfs.only:
			nd = os.path.join(todir,d)
			if nd not in compound.right_only:
				logging.debug('right_only append [%s]'%(nd))
				compound.right_only.append(nd)
		return compound

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

	def __cpcmd_call(self,cmd,pwddir,curdir):
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
			while curdir.startswith('/'):
				curdir = curdir[1:]
			if len(curdir) == 0:
				curdir = '.'
			cmd = ['bash',cmd,curdir]
			logging.info('cmd (%s) pwd [%s] curdir[%s]'%(cmd,pwddir,curdir))
			subprocess.check_call(cmd)
		finally:
			os.chdir(olddir)
		return

	def __remove_dir(self,dirn,issuper=False):
		if issuper:
			cmd = ['sudo','rm','-rf',dirn]
		else:
			cmd = ['rm','-rf',dirn]
		subprocess.check_call(cmd)
		return

	def cpin_call(self,pwddir,curdir):
		cpin = os.environ['CPIN_BIN']
		self.__cpcmd_call(cpin,pwddir,curdir)
		return

	def cpout_call(self,pwddir,curdir):
		cpout = os.environ['CPOUT_BIN']
		self.__cpcmd_call(cpout,pwddir,curdir)
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
				if cfs.left_diffs[i] not in crfromfiles:
					logging.warn('[%d][%s] not crfromfiles'%(i,cfs.left_diffs[i]))
				#self.assertTrue( cfs.left_diffs[i] in crfromfiles )
				cmpfs = CheckFiles(True)
				retval = cmpfs.check_file_same(cfs.left_diffs[i],cfs.right_diffs[i])
				self.assertEqual(retval,True)
		self.__remove_dir(todir)
		self.__remove_dir(fromdir)
		return

	def test_cpin_all(self):
		if 'CP_MAX_CNT' in os.environ.keys():
			maxnum = int(os.environ['CP_MAX_CNT'])
		else:
			maxnum = random.randint(1,3)
		for i in range(maxnum):
			self.__cpin_all()
		return

	def __cpout_all(self):
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
		crfromfiles = self.random_make_subs(todir,filenum)
		# now copy the file
		self.cpout_call(todir,'.')
		cfs = self.dircompare(fromdir,todir,False)
		self.assertEqual(cfs.left_only,[])
		self.assertEqual(cfs.right_only,[])
		self.assertEqual(len(cfs.left_diffs),len(cfs.right_diffs))
		if len(cfs.left_diffs) > 0:
			for i in range(len(cfs.left_diffs)):
				if cfs.left_diffs[i] not in crfromfiles:
					logging.warn('[%d][%s] not crfromfiles'%(i,cfs.left_diffs[i]))
				#self.assertTrue( cfs.left_diffs[i] in crfromfiles )
				cmpfs = CheckFiles(True)
				retval = cmpfs.check_file_same(cfs.left_diffs[i],cfs.right_diffs[i])
				self.assertEqual(retval,True)
		self.__remove_dir(todir)
		self.__remove_dir(fromdir,True)
		return

	def test_cpout_all(self):
		if 'CP_MAX_CNT' in os.environ.keys():
			maxnum = int(os.environ['CP_MAX_CNT'])
		else:
			maxnum = random.randint(1,3)
		for i in range(maxnum):
			self.__cpout_all()
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


	def make_random_link(self,fromdir,num):
		crfromfiles = []
		curdir = fromdir
		for i in range(num):
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
				curfile = make_templink(curdir)
				logging.debug('[%d]add link [%s]'%(len(crfromfiles),curfile))
				crfromfiles.append(curfile)
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
		crfromfiles = self.random_make_subs(fromdir,filenum)
		# now copy the file
		self.cpin_call(todir,'.')
		# now to make the 
		sdir,relpath = select_random_subdir(fromdir)
		crfromfiles = []
		filenum = random.randint(1,100)
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
				if cfs.left_diffs[i] not in crfromfiles:
					logging.warn('[%d][%s] not crfromfiles'%(i,cfs.left_diffs[i]))
				#self.assertTrue( cfs.left_diffs[i] in crfromfiles )
				cmpfs = CheckFiles(True)
				retval = cmpfs.check_file_same(cfs.left_diffs[i],cfs.right_diffs[i])
				self.assertEqual(retval,True)
		self.__remove_dir(todir)
		self.__remove_dir(fromdir)
		return

	def test_cpin_sub(self):
		if 'CP_MAX_CNT' in os.environ.keys():
			maxnum = int(os.environ['CP_MAX_CNT'])
		else:
			maxnum = random.randint(1,3)
		for i in range(maxnum):
			self.__cpin_sub()
		return

	def __cpout_sub(self):
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
		crfromfiles = self.random_make_subs(todir,filenum)
		# now copy the file
		self.cpout_call(todir,'.')
		# now to make the 
		sdir,relpath = select_random_subdir(todir)
		crfromfiles = []
		filenum = random.randint(1,100)
		crfromfiles = self.random_make_subs(sdir,filenum)

		self.cpout_call(todir,relpath)
		tosubdir = os.path.join(todir,relpath)
		fromsubdir = os.path.join(fromdir,relpath)
		cfs = self.dircompare(fromsubdir,tosubdir,False)
		self.assertEqual(cfs.left_only,[])
		self.assertEqual(cfs.right_only,[])
		self.assertEqual(len(cfs.left_diffs),len(cfs.right_diffs))
		if len(cfs.left_diffs) > 0:
			for i in range(len(cfs.left_diffs)):
				if cfs.left_diffs[i] not in crfromfiles:
					logging.warn('[%d][%s] not crfromfiles'%(i,cfs.left_diffs[i]))
				#self.assertTrue( cfs.left_diffs[i] in crfromfiles )
				cmpfs = CheckFiles(True)
				retval = cmpfs.check_file_same(cfs.left_diffs[i],cfs.right_diffs[i])
				self.assertEqual(retval,True)
		self.__remove_dir(todir)
		self.__remove_dir(fromdir,True)
		return

	def get_relpath(self,fromdir,fromsub):
		if  not fromsub.startswith(fromdir):
			raise Exception('fromsub [%s] not part [%s]'%(fromsub,fromdir))
		pathlen = len(fromdir)
		relpath = fromsub[pathlen:]
		if relpath[0] == '/':
			relpath = relpath[1:]
		return relpath


	def test_cpout_sub(self):
		if 'CP_MAX_CNT' in os.environ.keys():
			maxnum = int(os.environ['CP_MAX_CNT'])
		else:
			maxnum = random.randint(1,3)
		for i in range(maxnum):
			self.__cpout_sub()
		return


	def __cpout_subdir_notexists(self):
		# now first to make the dir to remove
		fromdir = os.environ['CP_SMB_DIR']
		todir = os.environ['CP_TO_DIR']
		# now we should make .git file
		# we should make this ok
		make_dir_safe(os.path.join(todir,'.git'))
		make_dir_safe(os.path.join(fromdir,'.git'))

				# now we make file
		filenum = random.randint(0,5)
		tomakedir = make_tempdir(todir)
		for i in range(filenum):
			tomakedir = make_tempdir(tomakedir)

		tofile = make_tempfile(tomakedir)
		basetodir = os.path.basename(todir)
		relpath = self.get_relpath(todir,tofile)
		fromfile = os.path.join(fromdir,basetodir,relpath)
		logging.info('todir[%s]basetodir[%s]tofile[%s]relpath[%s]fromfile[%s]'%(todir,basetodir,tofile,relpath,fromfile))
		self.cpout_call(todir,relpath)
		chkfile = CheckFiles(True)
		retval = chkfile.check_file_same(tofile,fromfile)
		self.assertEqual(retval,True)

		self.__remove_dir(fromdir,True)
		self.__remove_dir(todir)
		return

	def test_cpout_subdir_notexists(self):
		if 'CP_MAX_CNT' in os.environ.keys():
			maxnum = int(os.environ['CP_MAX_CNT'])
		else:
			maxnum = random.randint(1,3)
		for i in range(maxnum):
			self.__cpout_subdir_notexists()
		return

	def test_003(self):
		fromdir = os.environ['CP_TO_DIR']
		todir = os.environ['CP_SMB_DIR']
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
		# now we should make link
		crfromlinks = []
		crfromlinks = self.make_random_link(fromdir, filenum)
		self.cpout_call(fromdir,'.')
		cfs = self.dircompare(fromdir,todir,True)
		# now to check the different files
		self.assertEqual(len(cfs.left_only), len(crfromlinks))
		for f in cfs.left_only:
			self.assertTrue( f in crfromlinks)
		self.__remove_dir(fromdir)
		self.__remove_dir(todir,True)
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
    if logging.root and logging.root.handlers :
    	logging.root.handlers = []
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
	logging.info('CP_TO_DIR [%s] CP_SMB_DIR [%s] '%(os.environ['CP_TO_DIR'],os.environ['CP_SMB_DIR']))
	random.seed(time.time())
	sys.argv[1:] = args.args
	unittest.main(verbosity=args.verbose,failfast=args.failfast)
	return

if __name__ == '__main__':
	main()

