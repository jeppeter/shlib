#! /usr/bin/env python

import sys
import os
import extargsparse
import unittest
import logging
import cmdpack
import tempfile
import subprocess
import random
import time
import re
import platform


def make_dir_safe(dname=None):
	if dname is not None:
		if not os.path.isdir(dname):
			try:
				os.makedirs(dname)
			except:
				pass
			if not os.path.isdir(dname):
				raise Exception('can not make [%s]'%(dname))

def make_tempdir(prefix=None,suffix=''):
	make_dir_safe(prefix)
	d = tempfile.mkdtemp(suffix=suffix,dir=prefix)
	return os.path.abspath(os.path.realpath(d))

def make_tempfile(prefix=None,suffix=''):
	make_dir_safe(prefix)
	fd,result = tempfile.mkstemp(suffix=suffix,dir=prefix)
	os.close(fd)
	f = os.path.abspath(os.path.realpath(result))
	return f


def read_callback(rl,ctx):
	ctx.read_cmd(rl)
	return

class debug_testmak_case(unittest.TestCase):
	def setUp(self):
		if 'C' in os.environ.keys():
			del os.environ['C']
		if 'V' in os.environ.keys():
			del os.environ['V']
		return

	def tearDown(self):
		return

	@classmethod
	def setupClass(cls):
		return

	@classmethod
	def tearDownClass(cls):
		return

	def __format_make_common(self,s):
		return s + '\n'

	def __format_make_command(self,s,nooutput=True):
		rets = '\t'
		if nooutput:
			rets += '@'
		rets += s + '\n'
		return rets

	def __format_varaible_echo(self,varname,echobin='/bin/echo'):
		return self.__format_make_command('%s "%s ${%s}"'%(echobin,varname,varname))

	def __format_basedef_testmak(self,includedir,echobin='/bin/echo'):
		s = ''
		s += self.__format_make_common('include %s'%(os.path.join(includedir,'basedef.mak')))
		s += self.__format_make_common('')
		s += self.__format_make_common('all:')
		s += self.__format_varaible_echo('PERL',echobin)
		s += self.__format_varaible_echo('PYTHON',echobin)
		s += self.__format_varaible_echo('SED',echobin)
		s += self.__format_varaible_echo('SUDO',echobin)
		s += self.__format_varaible_echo('GCC',echobin)
		s += self.__format_varaible_echo('LD',echobin)
		s += self.__format_varaible_echo('ECHO',echobin)
		s += self.__format_varaible_echo('RM',echobin)
		s += self.__format_varaible_echo('CAT',echobin)
		s += self.__format_varaible_echo('PRINTF',echobin)
		s += self.__format_varaible_echo('LN',echobin)
		s += self.__format_varaible_echo('TRUE',echobin)
		s += self.__format_varaible_echo('TOUCH',echobin)
		return s

	def __write_file(self,s,f):
		#logging.debug('write [%s] <<<EOF\n%s\nEOF'%(f,s))
		with open(f,'w+b') as fout:
			fout.write('%s'%(s))
		return f



	def __write_tempfile(self,s,tmpdir='/tmp'):
		tempf = make_tempfile(tmpdir)
		self.__write_file(s,tempf)
		logging.debug('write [%s] << %s'%(tempf,s))
		return tempf

	def read_cmd(self,rl):
		logging.debug('rl [%s]'%(rl.rstrip('\r\n')))
		self.__output.append(rl)
		return

	def __run_command_output(self,cmds,stdoutcatch=True,stderrcatch=False):
		self.__output = []
		stdoutpipe = subprocess.PIPE
		stderrpipe = subprocess.PIPE
		if not stdoutcatch :
			stdoutpipe = open(os.devnull,'w')
		if not stderrcatch:
			if 'TEST_RESERVED' in os.environ.keys():
				stderrpipe = None
			else:
				stderrpipe = open(os.devnull,'w')
		logging.debug('run (%s)'%(cmds))
		logging.debug('PATH [%s]'%(os.environ['PATH']))
		retcode = cmdpack.run_command_callback(cmds,read_callback,self,stdoutpipe,stderrpipe)
		self.assertEqual(retcode,0)
		logging.debug('output (%s)'%(self.__output))
		if stdoutpipe != subprocess.PIPE and stdoutpipe is not None:
			stdoutpipe.close()
		if stderrpipe != subprocess.PIPE and stderrpipe is not None:
			stderrpipe.close()
		stdoutpipe = None
		stderrpipe = None
		return self.__output

	def __run_make(self,f,target=None,vardict=None):
		makebin = 'make'
		if 'MAKEBIN' in  os.environ.keys():
			makebin = os.environ['MAKEBIN']
		cmds = []
		cmds.append(makebin)
		cmds.append('--no-print-directory')
		cmds.append('-C')
		cmds.append('%s'%(os.path.dirname(f)))
		cmds.append('-f')
		cmds.append('%s'%(os.path.basename(f)))
		if vardict is not None:
			for c in vardict.keys():
				logging.debug('%s=%s'%(c,vardict[c]))
				cmds.append('%s=%s'%(c,vardict[c]))
		if target is not None:
			cmds.append(target)
		return self.__run_command_output(cmds)

	def __check_str_value(self,outsarr,s):
		cnt = 0
		#logging.debug('outsarr (%s) s[%s]'%(outsarr,s))
		for l in outsarr:
			if l.rstrip('\r\n') == s.rstrip('\r\n'):
				return cnt
			cnt += 1
		return -1

	def __get_which(self,binname):
		cmds = []
		cmds.append('which')
		cmds.append(binname)
		outsarr = self.__run_command_output(cmds)
		if len(outsarr) > 0:
			return outsarr[0]
		return None

	def __check_which_bin(self,binname,outsarr,varname=None):
		binpath = self.__get_which(binname)
		binvar = binname.upper()
		if varname is not None:
			binvar = varname
		s = '%s %s'%(binvar,binpath)
		return self.__check_str_value(outsarr,s)

	def __remove_dir(self,dirn,issuper=False):
		if issuper:
			cmd = ['sudo','rm','-rf',dirn]
		else:
			cmd = ['rm','-rf',dirn]
		subprocess.check_call(cmd)
		return


	def __remove_file_safe(self,f=None):
		if 'TEST_RESERVED' not in os.environ.keys() and f is not None:
			if os.path.exists(f):
				if os.path.isdir(f):
					logging.debug('remove %s'%(f))
					self.__remove_dir(f)
				else:
					logging.debug('remove %s'%(f))
					os.remove(f)
			else:
				logging.debug('[%s] not exists'%(f))
		else:
			logging.debug('not remove [%s]'%(f))
		return

	def __get_makelib_dir(self):
		makelibdir = os.path.dirname(os.path.realpath(__file__))
		if 'MAKELIB_DIR' in os.environ.keys():
			makelibdir = os.environ['MAKELIB_DIR']
		return makelibdir

	def test_001_basedef_case(self):
		testf=None
		try:
			makelibdir = self.__get_makelib_dir()
			s = self.__format_basedef_testmak(makelibdir)
			testf = self.__write_tempfile(s)
			outsarr = self.__run_make(testf,'all')
			idx = 0
			self.assertEqual(idx,self.__check_which_bin('perl',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('python',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('sed',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('sudo',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('gcc',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('ld',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('echo',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('rm',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('cat',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('printf',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('ln',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('true',outsarr))
			idx += 1
			self.assertEqual(idx,self.__check_which_bin('touch',outsarr))
		finally:
			self.__remove_file_safe(testf)
		return

	def __format_varop_testmak(self,includedir,longname):
		s = ''
		s += self.__format_make_common('include %s'%(os.path.join(includedir,'basedef.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(includedir,'varop.mak')))
		s += self.__format_make_common('')
		s += self.__format_make_common('ifeq (${C},)')
		s += self.__format_make_common('unexport CVALUE')
		s += self.__format_make_common('else')
		s += self.__format_make_common('CVALUE=${C}')
		s += self.__format_make_common('endif')
		s += self.__format_make_common('')
		s += self.__format_make_common('ifeq (${D},)')
		s += self.__format_make_common('unexport DVALUE')
		s += self.__format_make_common('else')
		s += self.__format_make_common('DVALUE=${D}')
		s += self.__format_make_common('endif')
		s += self.__format_make_common('')
		s += self.__format_make_common('ifeq (${E},)')
		s += self.__format_make_common('unexport EVALUE')
		s += self.__format_make_common('else')
		s += self.__format_make_common('EVALUE=${E}')
		s += self.__format_make_common('endif')
		s += self.__format_make_common('')
		s += self.__format_make_common('all:')
		s += self.__format_make_command('${ECHO} "VALUE2 $(call get_value_default,${CVALUE},default_c_value)"')
		s += self.__format_make_command('${ECHO} "VALUE3 $(call get_value_default_3,${CVALUE},${DVALUE},default_d_value)"')
		s += self.__format_make_command('${ECHO} "VALUE4 $(call get_value_default_4,${CVALUE},${DVALUE},${EVALUE},default_e_value)"')
		s += self.__format_make_command('${ECHO} "%s shortname $(call get_shortname,"%s")"'%(longname,longname))
		return s

	def __get_shortname(self,longname,basedir=None):
		
		if basedir is not None:
			shortname = longname
			shortname = shortname.replace(basedir,'')
			while shortname.startswith('/') or shortname.startswith('\\'):
				shortname = shortname[1:]
		else:
			shortname = os.path.basename(longname)
		shortname = shortname.replace('.','_')
		shortname = shortname.replace('/','_')
		shortname = shortname.replace('\\','_')
		return shortname


	def test_002_varop_case(self):
		testf = None
		try:
			makelibdir = self.__get_makelib_dir()
			longname = make_tempfile()
			s = self.__format_varop_testmak(makelibdir,longname)
			testf = self.__write_tempfile(s)
			outsarr = self.__run_make(testf,'all')
			self.assertEqual(len(outsarr),4)
			self.assertEqual(0,self.__check_str_value(outsarr,'VALUE2 default_c_value'))
			self.assertEqual(1,self.__check_str_value(outsarr,'VALUE3 default_d_value'))
			self.assertEqual(2,self.__check_str_value(outsarr,'VALUE4 default_e_value'))
			self.assertEqual(3,self.__check_str_value(outsarr,'%s shortname %s'%(longname,self.__get_shortname(longname))))
			vardict = dict()
			vardict['C'] = 'c_value_set'
			outsarr = self.__run_make(testf,'all',vardict)
			self.assertEqual(len(outsarr),4)
			self.assertEqual(0,self.__check_str_value(outsarr,'VALUE2 c_value_set'))
			self.assertEqual(1,self.__check_str_value(outsarr,'VALUE3 c_value_set'))
			self.assertEqual(2,self.__check_str_value(outsarr,'VALUE4 c_value_set'))
			self.assertEqual(3,self.__check_str_value(outsarr,'%s shortname %s'%(longname,self.__get_shortname(longname))))
			vardict = dict()
			vardict['D'] = 'd_value_set'
			outsarr = self.__run_make(testf,'all',vardict)
			self.assertEqual(len(outsarr),4)
			self.assertEqual(0,self.__check_str_value(outsarr,'VALUE2 default_c_value'))
			self.assertEqual(1,self.__check_str_value(outsarr,'VALUE3 d_value_set'))
			self.assertEqual(2,self.__check_str_value(outsarr,'VALUE4 d_value_set'))
			self.assertEqual(3,self.__check_str_value(outsarr,'%s shortname %s'%(longname,self.__get_shortname(longname))))
			vardict = dict()
			vardict['E'] = 'e_value_set'
			outsarr = self.__run_make(testf,'all',vardict)
			self.assertEqual(len(outsarr),4)
			self.assertEqual(0,self.__check_str_value(outsarr,'VALUE2 default_c_value'))
			self.assertEqual(1,self.__check_str_value(outsarr,'VALUE3 default_d_value'))
			self.assertEqual(2,self.__check_str_value(outsarr,'VALUE4 e_value_set'))
			self.assertEqual(3,self.__check_str_value(outsarr,'%s shortname %s'%(longname,self.__get_shortname(longname))))
		finally:
			self.__remove_file_safe(testf)
			self.__remove_file_safe(longname)
		return

	def __format_testexecmak(self,makelibdir,longname):
		s = ''
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'basedef.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'varop.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'exec.mak')))
		s += self.__format_make_common('')
		s += self.__format_make_common('all:')
		s += self.__format_make_command('$(call call_exec,${TRUE},"ECHO","hello")',False)
		s += self.__format_make_command('$(call call_exec,${TRUE},"ECHO","%s")'%(longname),False)
		return s

	def test_003_exec_case(self):
		testf = None
		longname = None
		try:
			makelibdir = self.__get_makelib_dir()
			longname = make_tempfile()
			s = self.__format_testexecmak(makelibdir,longname)
			testf = self.__write_tempfile(s)
			truebin = self.__get_which('true')
			outsarr = self.__run_make(testf,'all')
			self.assertEqual(len(outsarr),2)
			self.assertEqual(0,self.__check_str_value(outsarr,'    %-9s hello'%('ECHO')))
			self.assertEqual(1,self.__check_str_value(outsarr,'    %-9s %s'%('ECHO',longname)))
			vardict = dict()
			vardict['V']='1'
			outsarr = self.__run_make(testf,'all',vardict)
			self.assertEqual(len(outsarr),2)
			self.assertEqual(0,self.__check_str_value(outsarr,'%s'%(truebin)))
			self.assertEqual(0,self.__check_str_value(outsarr[1:],'%s'%(truebin)))
		finally:
			self.__remove_file_safe(testf)
			self.__remove_file_safe(longname)
		return

	def __format_testfileop(self,makelibdir,longname):
		s = ''
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'basedef.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'varop.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'exec.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'fileop.mak')))
		s += self.__format_make_common('')
		s += self.__format_make_common('CURDIR:=$(call readlink_f,.)')
		s += self.__format_make_common('BASENAME:=$(call get_basename,"%s")'%(longname))
		s += self.__format_make_common('')
		s += self.__format_make_common('all:')
		s += self.__format_make_command('$(call call_exec,${TRUE},"PWD","${CURDIR}")',False)
		s += self.__format_make_command('$(call call_exec,${TRUE},"BASE","${BASENAME}")',False)
		return s

	def test_004_fileop_case(self):
		testf = None
		longname = None
		try:
			makelibdir = self.__get_makelib_dir()
			longname = make_tempfile()
			s = self.__format_testfileop(makelibdir,'%s.suffix'%(longname))
			testf = self.__write_tempfile(s)
			outsarr = self.__run_make(testf,'all')
			truebin = self.__get_which('true')
			self.assertEqual(len(outsarr),2)
			self.assertEqual(0,self.__check_str_value(outsarr,'    %-9s %s'%('PWD',os.path.dirname(os.path.realpath(testf)))))
			self.assertEqual(1,self.__check_str_value(outsarr,'    %-9s %s'%('BASE',os.path.basename('%s.suffix'%(longname)))))
			vardict = dict()
			vardict['V']='1'
			outsarr = self.__run_make(testf,'all',vardict)
			self.assertEqual(len(outsarr),2)
			self.assertEqual(0,self.__check_str_value(outsarr,'%s'%(truebin)))
			self.assertEqual(0,self.__check_str_value(outsarr[1:],'%s'%(truebin)))
		finally:
			self.__remove_file_safe(testf)
			self.__remove_file_safe(longname)
		return

	def __get_random_max(self,maxnum,minnum=0):
		return random.randint(minnum,maxnum)

	def __get_relocate_path(self,fname,basedir):
		s = ''
		fullpath = os.path.realpath(fname)		
		s = fullpath
		if  basedir is not None and fullpath.startswith(basedir):
			s = fullpath.replace(basedir,'')
			while s.startswith('/') or s.startswith('\\'):
				s = s[1:]
		return s


	def __format_depop_make(self,makelibdir,basedir,cfilelist,Sfilelist,linkcfiles=None,linksfiles=None,mainexe='main',cflagname='CFLAGS',sflagname='ASMFLAG',ldflagname='LDFLAGS',includedir=[],definemacros=None,filespec=None):
		s = ''
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'basedef.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'varop.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'exec.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'fileop.mak')))
		s += self.__format_make_common('include %s'%(os.path.join(makelibdir,'depop.mak')))
		s += self.__format_make_common('')
		s += self.__format_make_common('CURDIR:=$(call readlink_f,.)')
		rets = 'c_srcs_basic ='
		s += self.__format_make_common('%s'%(rets))
		if len(cfilelist) > 0:
			rets = 'c_srcs_basic += '
			for i in range(len(cfilelist)):
				if (i%5) == 0 and i > 0:
					s += self.__format_make_common('%s'%(rets))
					rets = 'c_srcs_basic +='
				rets += ' %s'%(self.__get_relocate_path(cfilelist[i],basedir))
			if len(rets) > 0:
				s += self.__format_make_common('%s'%(rets))
		rets = ''
		s += self.__format_make_common('%s'%(rets))
		s += self.__format_make_common('c_srcs := $(patsubst %,${CURDIR}/%,${c_srcs_basic})')
		s += self.__format_make_common('c_objs := $(patsubst %.c,%.o,${c_srcs})')
		s += self.__format_make_common('c_deps := $(patsubst %,%.d,${c_srcs})')

		rets = 'link_c_srcs_basic ='
		s += self.__format_make_common('%s'%(rets))
		if linkcfiles is not None:
			linkcs = sorted(linkcfiles.keys())
			rets = 'link_c_srcs_basic += '
			for i in range(len(linkcs)):
				if (i%5) == 0 and i > 0:
					s += self.__format_make_common('%s'%(rets))
					rets = 'link_c_srcs_basic += '
				rets += ' %s'%(self.__get_relocate_path(linkcs[i],basedir))
			if len(rets) > 0:
				s += self.__format_make_common('%s'%(rets))
		rets = ''
		s += self.__format_make_common('%s'%(rets))
		s += self.__format_make_common('link_c_srcs := $(patsubst %,${CURDIR}/%,${link_c_srcs_basic})')
		s += self.__format_make_common('link_c_objs := $(patsubst %.c,%.o,${link_c_srcs})')
		s += self.__format_make_common('link_c_deps := $(patsubst %,%.d,${link_c_srcs})')

		if linkcfiles is not None:
			sortedkeys = sorted(linkcfiles.keys())
			for c in sortedkeys:
				s += self.__format_make_common('%s_SRC := ${CURDIR}/%s'%(self.__get_shortname(c,basedir),self.__get_relocate_path(linkcfiles[c],basedir)))

		rets = 'S_srcs_basic = '
		s += self.__format_make_common('%s'%(rets))
		if len(Sfilelist) >0:
			rets = 'S_srcs_basic += '
			for i in range(len(Sfilelist)):
				if (i % 5) == 0 and i > 0:
					s += self.__format_make_common('%s'%(rets))
					rets = 'S_srcs_basic += '
				rets += ' %s'%(self.__get_relocate_path(Sfilelist[i],basedir))
			if len(rets) > 0:
				s += self.__format_make_common('%s'%(rets))
		rets = ''
		s += self.__format_make_common('%s'%(rets))
		s += self.__format_make_common('S_srcs := $(patsubst %,${CURDIR}/%,${S_srcs_basic})')
		s += self.__format_make_common('S_objs := $(patsubst %.S,%.o,${S_srcs})')
		s += self.__format_make_common('S_deps := $(patsubst %,%.d,${S_srcs})')

		rets = 'link_S_srcs_basic ='
		s += self.__format_make_common('%s'%(rets))
		if linksfiles is not None:
			linkss = sorted(linksfiles.keys())
			rets = 'link_S_srcs_basic += '
			for i in range(len(linkss)):
				if (i%5) == 0 and i > 0:
					s += self.__format_make_common('%s'%(rets))
					rets = 'link_S_srcs_basic += '
				rets += ' %s'%(self.__get_relocate_path(linkss[i],basedir))
			if len(rets) > 0:
				s += self.__format_make_common('%s'%(rets))
		rets = ''
		s += self.__format_make_common('%s'%(rets))
		s += self.__format_make_common('link_S_srcs := $(patsubst %,${CURDIR}/%,${link_S_srcs_basic})')
		s += self.__format_make_common('link_S_objs := $(patsubst %.S,%.o,${link_S_srcs})')
		s += self.__format_make_common('link_S_deps := $(patsubst %,%.d,${link_S_srcs})')

		if linksfiles is not None:
			sortedkeys = sorted(linksfiles.keys())
			for c in sortedkeys:
				s += self.__format_make_common('%s_SRC := ${CURDIR}/%s'%(self.__get_shortname(c,basedir),self.__get_relocate_path(linksfiles[c],basedir)))


		s += self.__format_make_common('objs := ${c_objs} ${S_objs} ${link_c_objs} ${link_S_objs}')
		s += self.__format_make_common('deps := ${c_deps} ${S_deps} ${link_c_deps} ${link_S_deps}')
		s += self.__format_make_common('')

		s += self.__format_make_common('%s = -Wall '%(cflagname))
		if len(includedir) > 0:
			for c in includedir:
				s += self.__format_make_common('%s += -I${CURDIR}/%s'%(cflagname,self.__get_relocate_path(c,basedir)))

		if definemacros is not None:
			for c in definemacros.keys():
				s += self.__format_make_common('%s += -D%s=%s'%(cflagname,c,definemacros[c]))


		s += self.__format_make_common('%s = ${%s} -D__ASSEMBLY__'%(sflagname,cflagname))


		if filespec is not None:
			for c in filespec.keys():
				s += self.__format_make_common('%s_CFLAGS += %s'%(self.__get_shortname(c,basedir),filespec[c]))


		s += self.__format_make_common('%s = -Wall '%(ldflagname))

		s += self.__format_make_common('')
		s += self.__format_make_common('all:%s'%(mainexe))
		s += self.__format_make_common('')
		s += self.__format_make_common('%s:${objs}'%(mainexe))
		s += self.__format_make_command('$(call call_exec,${GCC} ${%s} -o %s ${objs},"LD","%s")'%(ldflagname,mainexe,mainexe),False)

		s += self.__format_make_common('')
		#s += self.__format_make_common('-include ${deps}')
		if len(cfilelist) > 0:
			s += self.__format_make_common('')
			s += self.__format_make_common('$(call foreach_c_file_shortname,${c_srcs},${CURDIR},${%s},${GCC})'%(cflagname))
			s += self.__format_make_common('')

		if linkcfiles is not None:
			s += self.__format_make_common('')
			s += self.__format_make_common('$(call foreach_link_c_file_shortname,${link_c_srcs},${CURDIR},${%s},${GCC})'%(cflagname))
			s += self.__format_make_common('')

		if len(Sfilelist) > 0:
			s += self.__format_make_common('')
			s += self.__format_make_common('$(call foreach_S_file_shortname,${S_srcs},${CURDIR},${%s},${GCC})'%(sflagname))
			s += self.__format_make_common('')

		if linksfiles is not None:
			s += self.__format_make_common('')
			s += self.__format_make_common('$(call foreach_link_S_file_shortname,${link_S_srcs},${CURDIR},${%s},${GCC})'%(cflagname))
			s += self.__format_make_common('')

		s += self.__format_make_common('clean:')
		s += self.__format_make_command('$(call call_exec,${RM} -f %s,"RM","%s")'%(mainexe,mainexe),False)
		s += self.__format_make_command('$(call call_exec,${RM} -f ${deps},"RM","deps")',False)
		s += self.__format_make_command('$(call call_exec,${RM} -f ${objs},"RM","objs")',False)
		s += self.__format_make_command('$(call call_exec,${RM} -f ${link_c_srcs},"RM","linkc")',False)
		s += self.__format_make_command('$(call call_exec,${RM} -f ${link_S_srcs},"RM","links")',False)
		#for c in linkcfiles.keys():
		#	s += self.__format_make_command('$(call call_exec,${RM} -f ${CURDIR}/%s,"RM","$(call get_basename,${CURDIR}/%s)")'%(self.__get_relocate_path(c,basedir),
		#		self.__get_relocate_path(c,basedir)),False)
		return s

	def __get_define_macro(self,fname,basedir):
		s = ''
		s = fname.replace(basedir,'')
		s = s.replace('\\','_')
		s = s.replace('/','_')
		s = s.replace('.','_')
		s = s.upper()
		s = '__%s__'%(s)
		return s

	def __get_file_relative(self,fname,basedir):
		s = ''
		s = fname.replace(basedir,'')
		s = s.replace('\\','/')
		while len(s) > 0 and (s[0] == '/' or s[0] == '\\') :
			s = s[1:]
		return s

	def __make_header_s(self,fname,basedir,includeothers=[]):
		s = ''
		macro = self.__get_define_macro(fname,basedir)
		s += self.__format_make_common('#ifndef %s'%(macro))
		s += self.__format_make_common('#define %s'%(macro))
		s += self.__format_make_common('')
		for c in includeothers:
			s += self.__format_make_common('#include <%s>'%(self.__get_file_relative(c,basedir)))
		s += self.__format_make_common('')
		s += self.__format_make_common('#endif /*%s*/'%(macro))
		return s

	def __make_c_s(self,fname,includedir,includes=[]):
		s = ''
		for c in includes:
			s += self.__format_make_common('#include <%s>'%(self.__get_file_relative(c,includedir)))
		return s

	def __make_main_c_s(self,exename,fname,includedir,includes=[]):
		s = self.__make_c_s(fname,includedir,includes)
		s += self.__format_make_common('#include <stdio.h>')
		s += self.__format_make_common('')
		s += self.__format_make_common('int main(int argc,char* argv[])')
		s += self.__format_make_common('{')
		s += self.__format_make_common('\tprintf("%s called\\n");'%(exename))
		s += self.__format_make_common('\treturn 0;')
		s += self.__format_make_common('}')
		return s


	def __get_include_files(self,allfiles):
		if len(allfiles) > 1:
			rn = self.__get_random_max(len(allfiles)-1,0)
		else:
			rn = 0
		includes = []
		if rn > 0 :
			while len(includes) < rn:
				curfile = random.choice(allfiles)
				if curfile not in includes:
					includes.append(curfile)
		return includes

	def __get_use_max_cnt(self):
		maxnum = 200
		if 'TEST_MAXNUM' in os.environ.keys():
			maxnum = int(os.environ['TEST_MAXNUM'])
		return maxnum

	def __get_use_min_cnt(self):
		minnum = 20
		if 'TEST_MINNUM' in os.environ.keys():
			minnum = int(os.environ['TEST_MINNUM'])
		return minnum


	def __make_headers(self,includedir):
		maxfiles = self.__get_random_max(self.__get_use_max_cnt(),self.__get_use_min_cnt())
		files = dict()
		curdir = includedir
		while len(files.keys()) < maxfiles:
			rn = self.__get_random_max(20)
			if rn == 0:
				curdir = os.path.realpath(os.path.join(curdir,'..'))
				if len(curdir) < len(includedir):
					curdir = includedir
			elif rn == 1:
				curdir = make_tempdir(curdir)
			else:
				includefiles = self.__get_include_files(files.keys())
				curfile = make_tempfile(curdir,'.h')
				s = self.__make_header_s(curfile,includedir,includefiles)
				self.__write_file(s,curfile)
				files[curfile] = includefiles
		return files

	def __make_c_files(self,mainexe,basedir,includefiles,includedir=None,cdir=None):
		maxc = self.__get_random_max(self.__get_use_max_cnt(),self.__get_use_min_cnt())
		cfiles = dict()
		if cdir is None:
			cdir = os.path.join(basedir,'src')
		if includedir is None:
			includedir = os.path.join(basedir,'include')
		curdir = cdir
		while len(cfiles.keys()) < maxc:
			rn = self.__get_random_max(20)
			if rn == 0:
				curdir = os.path.realpath(os.path.join(curdir,'..'))
				if len(curdir) < len(cdir):
					curdir = cdir
			elif rn == 1:
				curdir = make_tempdir(curdir)
			else:
				curincludes = self.__get_include_files(includefiles)
				curfile = make_tempfile(curdir,'.c')
				s = self.__make_c_s(curfile,includedir,curincludes)
				self.__write_file(s,curfile)
				cfiles[curfile] = curincludes
		curfile = make_tempfile(curdir,'.c')
		curincludes = self.__get_include_files(includefiles)
		s = self.__make_main_c_s(mainexe,curfile,includedir,curincludes)
		self.__write_file(s,curfile)
		cfiles[curfile] = curincludes
		return  cfiles

	def __make_link_c_files(self,basedir,cfiles,cdir=None,linkdir=None):
		linked = dict()
		if cdir is None:
			cdir = os.path.join(basedir,'src')
		if linkdir is None:
			linkdir = os.path.join(basedir,'link')
		curdir = linkdir
		maxlink = self.__get_random_max(self.__get_use_max_cnt(),self.__get_use_min_cnt())
		while len(linked.keys()) < maxlink:
			rn = self.__get_random_max(20)
			if rn == 0:
				curdir = os.path.realpath(os.path.join(curdir,'..'))
				if len(curdir) < len(linkdir):
					curdir = linkdir
			elif rn == 1:
				curdir = make_tempdir(curdir)
			else:
				curfile = make_tempfile(curdir,'.c')
				if curfile not in linked.keys():
					if (len(cfiles) == 0):
						# nothing to make
						os.remove(curfile)
						break
					cursrc = random.choice(cfiles)
					linked[curfile] = cursrc
					logging.debug('[%s] linked [%s]'%(curfile,cursrc))
					cfiles.remove(cursrc)
					os.remove(curfile)
		return linked

	def __make_link_S_files(self,basedir,sfiles,sdir=None,linkdir=None):
		linked = dict()
		if sdir is None:
			sdir = os.path.join(basedir,'asm')
		if linkdir is None:
			linkdir = os.path.join(basedir,'linkS')
		curdir = linkdir
		maxlink = self.__get_random_max(self.__get_use_max_cnt(),self.__get_use_min_cnt())
		while len(linked.keys()) < maxlink:
			rn = self.__get_random_max(20)
			if rn == 0:
				curdir = os.path.realpath(os.path.join(curdir,'..'))
				if len(curdir) < len(linkdir):
					curdir = linkdir
			elif rn == 1:
				curdir = make_tempdir(curdir)
			else:
				curfile = make_tempfile(curdir,'.S')
				if curfile not in linked.keys():
					if (len(sfiles) == 0):
						# nothing to make
						os.remove(curfile)
						break
					cursrc = random.choice(sfiles)
					linked[curfile] = cursrc
					logging.debug('[%s] linked [%s]'%(curfile,cursrc))
					sfiles.remove(cursrc)
					os.remove(curfile)
		return linked

	def __make_S_files(self,basedir,includefiles,includedir=None,sdir=None):
		if includedir is None:
			includedir = os.path.join(basedir,'include')
		if sdir is None:
			sdir = os.path.join(basedir,'asm')
		maxs = self.__get_random_max(self.__get_use_max_cnt(),self.__get_use_min_cnt())
		sfiles = dict()
		curdir = sdir
		while len(sfiles.keys()) < maxs:
			rn = self.__get_random_max(20)
			if rn == 0:
				curdir = os.path.realpath(os.path.join(curdir,'..'))
				if len(curdir) < len(sdir):
					curdir = sdir
			elif rn == 1:
				curdir = make_tempdir(curdir)
			else:
				curfile = make_tempfile(curdir,'.S')
				includes = self.__get_include_files(includefiles)
				s = self.__make_c_s(curfile,includedir,includes)				
				self.__write_file(s,curfile)
				sfiles[curfile] = includes
		return sfiles

	def __get_basename(self,c):
		return os.path.basename(c)

	def __format_exec_output(self,verb,cont):
		return '    %-9s %s'%(verb,cont)

	def __check_link_c_files_link_deps(self,outsarr,startidx,linkcfiles=None,affectlc=None):
		curidx = startidx
		if linkcfiles is not None:
			if affectlc is None:
				sortedkeys = sorted(linkcfiles.keys())
			else:
				sortedkeys = sorted(affectlc)
			i = len(sortedkeys) - 1
			while i >= 0:
				curs = self.__format_exec_output('LINK',self.__get_basename(sortedkeys[i]))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				curidx += 1
				curs = self.__format_exec_output('DEPS','%s.d'%(self.__get_basename(sortedkeys[i])))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				curidx += 1
				i -= 1
		return curidx


	def __check_link_S_files_link_deps(self,outsarr,startidx,linksfiles=None,affectls=None):
		curidx = startidx
		if linksfiles is not None:
			if affectls is None:
				sortedkeys = sorted(linksfiles.keys())
			else:
				sortedkeys = sorted(affectls)
			i = len(sortedkeys) - 1
			while i >= 0:
				curs = self.__format_exec_output('LINK',self.__get_basename(sortedkeys[i]))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				curidx += 1
				curs = self.__format_exec_output('DEPS','%s.d'%(self.__get_basename(sortedkeys[i])))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				curidx += 1
				i -= 1
		return curidx


	def __check_S_files_deps(self,outsarr,startidx,sfiles):
		curidx = startidx
		if len(sfiles) > 0:
			i = len(sfiles) - 1
			while i >=0 :
				curs = self.__format_exec_output('DEPS','%s.d'%(self.__get_basename(sfiles[i])))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				curidx += 1
				i -= 1
		return curidx

	def __check_c_files_deps(self,outsarr,startidx,cfiles):
		curidx = startidx
		if len(cfiles) > 0:
			i = len(cfiles) - 1
			while i >= 0:
				curs = self.__format_exec_output('DEPS','%s.d'%(self.__get_basename(cfiles[i])))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				i -= 1
				curidx += 1
		return curidx

	def __get_to_o(self,fname):
		s = self.__get_basename(fname)
		s = re.sub('\.[cS]$','.o',s)
		return s

	def __check_c_files_cc(self,outsarr,startidx,cfiles):
		curidx = startidx
		if len(cfiles) > 0:
			i = 0
			while i < len(cfiles):
				curs = self.__format_exec_output('CC','%s'%(self.__get_to_o(cfiles[i])))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				i += 1
				curidx += 1
		return curidx

	def __check_S_files_cc(self,outsarr,startidx,sfiles):
		curidx = startidx
		if len(sfiles) > 0:
			i = 0
			while i < len(sfiles):
				curs = self.__format_exec_output('AS','%s'%(self.__get_to_o(sfiles[i])))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				i += 1
				curidx += 1
		return curidx

	def __check_link_c_files_cc(self,outsarr,startidx,linkcfiles=None,affectlc=None):
		curidx = startidx
		if linkcfiles is not None:
			if affectlc is None:
				sortedlinks = sorted(linkcfiles.keys())
			else:
				sortedlinks = sorted(affectlc)
			i = 0
			while i < len(sortedlinks):
				curs = self.__format_exec_output('CC','%s'%(self.__get_to_o(sortedlinks[i])))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				curidx += 1
				i += 1
		return curidx

	def __check_link_S_files_cc(self,outsarr,startidx,linksfiles=None,affectls=None):
		curidx = startidx
		if linksfiles is not None:
			if affectls is None:
				sortedlinks = sorted(linksfiles.keys())
			else:
				sortedlinks = sorted(affectls)
			i = 0
			while i < len(sortedlinks):
				curs = self.__format_exec_output('AS','%s'%(self.__get_to_o(sortedlinks[i])))
				logging.debug('curidx[%d][%d] [%s]'%(curidx,i,curs))
				self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
				curidx += 1
				i += 1
		return curidx


	def __check_ld_main(self,outsarr,startidx,mainexe):
		curidx = startidx
		curs = self.__format_exec_output('LD',mainexe)
		logging.debug('curidx[%d] [%s]'%(curidx,curs))
		self.assertEqual(0,self.__check_str_value(outsarr[curidx:],curs))
		curidx += 1
		return curidx

	def touch_file(self,infile):
		with open(infile,'r'):
			os.utime(infile,None)
		return

	def sorted_and_uniq(self,arr):
		sortarr = sorted(arr)
		i = 0
		while i < len(sortarr):
			if i < (len(sortarr)-1):
				if sortarr[i] == sortarr[i+1]:
					del sortarr[i+1]
					continue
			i += 1
		return sortarr

	def select_touch_files(self,hfiles,cfiles,sfiles,linkcfiles,linksfiles):
		touchincs = []
		touchcs = []
		touchss = []
		rn = self.__get_random_max(self.__get_use_max_cnt(),self.__get_use_min_cnt())
		linksrcc = []
		if linkcfiles is not None:
			for c in linkcfiles.keys():
				linksrcc.append(linkcfiles[c])
		linksrcs = []
		if linksfiles is not None:
			for c in linksfiles.keys():
				linksrcs.append(linksfiles[c])
		for i in range(rn):
			cn = self.__get_random_max(5)
			if cn == 0:
				if len(hfiles) > 0:
					touchincs.append(random.choice(hfiles))
			elif cn == 1:
				if len(cfiles) > 0:
					touchcs.append(random.choice(cfiles))
			elif cn == 2:
				if len(sfiles) > 0:
					touchss.append(random.choice(sfiles))
			elif cn == 3:
				if len(linksrcc) > 0:
					touchcs.append(random.choice(linksrcc))
			elif cn == 4:
				if len(linksrcs) > 0:
					touchss.append(random.choice(linksrcs))

		touchincs = self.sorted_and_uniq(touchincs)
		touchss = self.sorted_and_uniq(touchss)
		touchcs = self.sorted_and_uniq(touchcs)
		for c in touchincs:
			self.touch_file(c)
		for c in touchcs:
			self.touch_file(c)
		for c in touchss:
			self.touch_file(c)
		return touchincs,touchcs,touchss

	def __get_affected_cfiles(self,cdict,chgincludes,validcfiles):
		caffects = []
		for c in validcfiles:
			curincs = cdict[c]
			for cc in curincs:
				if cc in chgincludes :
					logging.debug('add[%s] because [%s]'%(c,cc))
					caffects.append(c)	
		return caffects

	def __get_affected_sfiles(self,sdict,chgincludes,validsfiles):
		checks = []
		for s in validsfiles:
			curincs = sdict[s]
			for ss in curincs:
				if ss in chgincludes:
					logging.debug('add [%s] because [%s]'%(s,ss))
					checks.append(s)
		return checks

	def __get_array(self,arr):
		s = '['
		for i in range(len(arr)):
			if i > 0:
				s += ' '
			s += '\'%s\''%(arr[i])
		s += ']'
		return s

	def __get_affected_linkcfiles(self,linkcfiles,cfiles,cdict,chgincludes):
		linkaffects = []
		if linkcfiles is not None:
			for c in linkcfiles.keys():
				linksrc = linkcfiles[c]
				if linksrc in cfiles:
					logging.debug('add[%s] because [%s]'%(c,linksrc))
					linkaffects.append(c)
				hfiles = cdict[linksrc]
				for h in hfiles:
					if h in chgincludes:
						logging.debug('add[%s] because [%s]'%(c,h))
						linkaffects.append(c)
		return linkaffects


	def __get_affected_linksfiles(self,linksfiles,sfiles,sdict,chgincludes):
		linkaffects = []
		if linksfiles is not None:
			for c in linksfiles.keys():
				linksrc = linksfiles[c]
				if linksrc in sfiles:
					logging.debug('add[%s] because [%s]'%(c,linksrc))
					linkaffects.append(c)
				hfiles = sdict[linksrc]
				for h in hfiles:
					if h in chgincludes:
						logging.debug('add[%s] because [%s]'%(c,h))
						linkaffects.append(c)
		return linkaffects

	def make_header_expand(self,hdict,chgincludes):
		retincs = chgincludes
		cont = True
		while cont:
			cont = False
			for k in hdict.keys():
				hfiles = hdict[k]
				for h in hfiles:
					if h in retincs and k not in retincs:
						logging.debug('add[%s] because [%s]'%(k,h))
						retincs.append(k)
						cont = True
		return retincs



	def test_005_depop_case(self):
		random.seed(time.time())
		basedir = None
		longname = None
		osname = platform.uname()[0].lower()
		try:
			basedir = make_tempdir()
			headdir = make_tempdir(basedir)
			cdir = make_tempdir(basedir)
			linkdir = make_tempdir(basedir)
			sdir = make_tempdir(basedir)
			linksdir = make_tempdir(basedir)
			headerfiles = self.__make_headers(headdir)
			longname = make_tempfile(basedir)
			mainexe = self.__get_shortname(longname)
			cfiles = self.__make_c_files(mainexe,basedir,headerfiles.keys(),headdir,cdir)
			linkcfiles = self.__make_link_c_files(basedir,cfiles.keys(),cdir,linkdir)
			sfiles = self.__make_S_files(basedir,headerfiles.keys(),headdir,sdir)
			linksfiles = self.__make_link_S_files(basedir,sfiles.keys(),sdir,linksdir)
			makelibdir = self.__get_makelib_dir()
			sortedcfiles = sorted(cfiles.keys())
			sortedsfiles = sorted(sfiles.keys())
			sortedhfiles = sorted(headerfiles.keys())
			sortedsfiles = sorted(sfiles.keys())
			for k in linkcfiles.keys():
				linksrc = linkcfiles[k]
				if linksrc in sortedcfiles:
					sortedcfiles.remove(linksrc)
			for k in linksfiles.keys():
				linksrc = linksfiles[k]
				if linksrc in sortedsfiles:
					sortedsfiles.remove(linksrc)
			s = self.__format_depop_make(makelibdir,basedir,sortedcfiles,sortedsfiles,linkcfiles,linksfiles,mainexe,'CFLAGS','ASMFLAG','LDFLAGS',includedir=[headdir])
			makefile = os.path.join(basedir,'Makefile')
			self.__write_file(s,makefile)
			# we remove the file 
			os.remove(longname)
			outsarr = self.__run_make(makefile,'all')
			# now we should get the output for handle
			curidx = 0
			curidx = self.__check_link_S_files_link_deps(outsarr,curidx,linksfiles)
			curidx = self.__check_S_files_deps(outsarr,curidx,sortedsfiles)
			curidx = self.__check_link_c_files_link_deps(outsarr,curidx,linkcfiles)
			curidx = self.__check_c_files_deps(outsarr,curidx,sortedcfiles)
			curidx = self.__check_c_files_cc(outsarr,curidx,sortedcfiles)
			curidx = self.__check_S_files_cc(outsarr,curidx,sortedsfiles)
			curidx = self.__check_link_c_files_cc(outsarr,curidx,linkcfiles)
			curidx = self.__check_link_S_files_cc(outsarr,curidx,linksfiles)
			curidx = self.__check_ld_main(outsarr,curidx,mainexe)
			outsarr = self.__run_make(makefile,'all')
			# nothing to do any more
			self.assertEqual(1,len(outsarr))
			matchexpr = re.compile('make(\[\d+\])?: Nothing to be done for `%s\'.'%('all'))
			ok = False
			if matchexpr.match(outsarr[0]):
				ok = True
			else:
				logging.error('outsarr (%s)'%(self.__get_array(outsarr)))
			self.assertEqual(ok,True)
			# now we should test for part change
			touchincs,touchcs,touchss = self.select_touch_files(sortedhfiles,sortedcfiles,sortedsfiles,linkcfiles,linksfiles)
			logging.debug('touchincs (%s)'%(self.__get_array(touchincs)))
			logging.debug('touchcs (%s)'%(self.__get_array(touchcs)))
			logging.debug('touchss (%s)'%(self.__get_array(touchss)))
			touchincs = self.make_header_expand(headerfiles,touchincs)			
			checkc = self.__get_affected_cfiles(cfiles,touchincs,sortedcfiles)
			if osname == 'darwin':
				# in darwin gcc ,it include the original file in depends ,so we do this
				for c in touchcs:
					if c not in linkcfiles.values():
						checkc.append(c)

			checks = self.__get_affected_sfiles(sfiles,touchincs,sortedsfiles)
			if osname == 'darwin':
				for c in touchss:
					# in darwin gcc ,it include the original file in depends ,so we do this
					if c not in linksfiles.values():
						checks.append(c)

			allcfiles = []
			for c in touchcs:
				allcfiles.append(c)
			allcfiles.extend(checkc)
			allcfiles = self.sorted_and_uniq(allcfiles)
			affectlc = self.__get_affected_linkcfiles(linkcfiles,allcfiles,cfiles,touchincs)

			affectlc = self.sorted_and_uniq(affectlc)
			checkc = self.sorted_and_uniq(checkc)

			checks = self.sorted_and_uniq(checks)
			allsfiles = []
			for c in touchss:
				allsfiles.append(c)
			allsfiles.extend(checks)
			affectls = self.__get_affected_linksfiles(linksfiles,allsfiles,sfiles,touchincs)

			affectls = self.sorted_and_uniq(affectls)


			logging.debug('touchincs (%s)'%(self.__get_array(touchincs)))
			logging.debug('touchcs (%s)'%(self.__get_array(touchcs)))
			logging.debug('touchss (%s)'%(self.__get_array(touchss)))
			logging.debug('checkc (%s)'%(self.__get_array(checkc)))
			logging.debug('checks (%s)'%(self.__get_array(checks)))
			logging.debug('affectlc (%s)'%(self.__get_array(affectlc)))
			logging.debug('affectls (%s)'%(self.__get_array(affectls)))
			# now we should make the affected to handle change
			outsarr = self.__run_make(makefile,'all')
			curidx = 0
			curidx = self.__check_link_S_files_link_deps(outsarr,curidx,linksfiles,affectls)
			curidx = self.__check_S_files_deps(outsarr,curidx,checks)
			curidx = self.__check_link_c_files_link_deps(outsarr,curidx,linkcfiles,affectlc)
			curidx = self.__check_c_files_deps(outsarr,curidx,checkc)

			compilec = checkc
			for c in touchcs:
				if c in sortedcfiles:
					compilec.append(c)			

			compilec = self.sorted_and_uniq(compilec)
			logging.debug('compilec (%s)'%(self.__get_array(compilec)))

			curidx = self.__check_c_files_cc(outsarr,curidx,compilec)

			compiles = checks
			logging.debug('compiles (%s)'%(self.__get_array(compiles)))
			for c in touchss:
				if c in sortedsfiles:
					logging.debug('add[%s]'%(c))
					compiles.append(c)
			compiles = self.sorted_and_uniq(compiles)
			logging.debug('compiles (%s)'%(self.__get_array(compiles)))
			curidx = self.__check_S_files_cc(outsarr,curidx,compiles)
			curidx = self.__check_link_c_files_cc(outsarr,curidx,linkcfiles,affectlc)
			curidx = self.__check_link_S_files_cc(outsarr,curidx,linksfiles,affectls)
			if len(affectls) > 0 or len(affectlc) > 0 or len(compiles) > 0 or len(compilec) > 0:
				curidx = self.__check_ld_main(outsarr,curidx,mainexe)
		finally:
			self.__remove_file_safe(basedir)
		return

	def test_006_makelib_case(self):
		makelibdir = self.__get_makelib_dir()
		exampledir = os.path.join(makelibdir,'example')
		for root,dirs,files in os.walk(exampledir):
			for d in dirs:
				makefile = os.path.join(root,d,'Makefile')
				if os.path.exists(makefile):
					self.__run_make(makefile,'clean')
					self.__run_make(makefile,'all')
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
		"makebin|m" : "make",
		"reserved|r" : false,
		"makelibdir|d" : "%s",
		"maxnum" : 8,
		"minnum" : 3,
		"$" : "*"
	}
	''' 
	commandline = commandline_fmt%(os.path.dirname(os.path.realpath(__file__)))
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	set_log_level(args)
	sys.argv[1:] = args.args
	os.environ['TEST_MAXNUM'] = '%s'%(args.maxnum)
	os.environ['TEST_MINNUM'] = '%s'%(args.minnum)
	if args.reserved : 
		os.environ['TEST_RESERVED'] = '1'
	else:
		if 'TEST_RESERVED' in os.environ.keys():
			del os.environ['TEST_RESERVED']
	unittest.main(verbosity=args.verbose,failfast=args.failfast)
	return

if __name__ == '__main__':
	main()
