#! /usr/bin/env python

import sys
import os
import extargsparse
import unittest
import logging
import cmdpack
import tempfile
import subprocess


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
		s += self.__format_varaible_echo('OBJCOPY',echobin)
		s += self.__format_varaible_echo('ECHO',echobin)
		s += self.__format_varaible_echo('RM',echobin)
		s += self.__format_varaible_echo('CAT',echobin)
		s += self.__format_varaible_echo('PRINTF',echobin)
		s += self.__format_varaible_echo('LN',echobin)
		s += self.__format_varaible_echo('TRUE',echobin)
		s += self.__format_varaible_echo('TOUCH',echobin)
		return s


	def __write_tempfile(self,s,tmpdir='/tmp'):
		tempfile = make_tempfile(tmpdir)
		with open(tempfile,'w+b') as f:
			f.write('%s'%(s))
		logging.debug('write [%s] << %s'%(tempfile,s))
		return tempfile

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
			stderrpipe = None
		logging.debug('run (%s)'%(cmds))
		logging.debug('PATH [%s]'%(os.environ['PATH']))
		retcode = cmdpack.run_command_callback(cmds,read_callback,self,stdoutpipe,stderrpipe)
		self.assertEqual(retcode,0)
		logging.debug('output (%s)'%(self.__output))
		if stdoutpipe != subprocess.PIPE and stdoutpipe is not None:
			stdoutpipe.close()
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
				cmds.append('%s=%s'%(c,vardict[c]))
		if target is not None:
			cmds.append(target)
		return self.__run_command_output(cmds)

	def __check_str_value(self,outsarr,s):
		cnt = 0
		logging.debug('outsarr (%s) s[%s]'%(outsarr,s))
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

	def test_basedef_case(self):
		testf=None
		try:
			makelibdir = self.__get_makelib_dir()
			s = self.__format_basedef_testmak(makelibdir)
			testf = self.__write_tempfile(s)
			outsarr = self.__run_make(testf,'all')
			self.assertEqual(0,self.__check_which_bin('perl',outsarr))
			self.assertEqual(1,self.__check_which_bin('python',outsarr))
			self.assertEqual(2,self.__check_which_bin('sed',outsarr))
			self.assertEqual(3,self.__check_which_bin('sudo',outsarr))
			self.assertEqual(4,self.__check_which_bin('gcc',outsarr))
			self.assertEqual(5,self.__check_which_bin('ld',outsarr))
			self.assertEqual(6,self.__check_which_bin('objcopy',outsarr))
			self.assertEqual(7,self.__check_which_bin('echo',outsarr))
			self.assertEqual(8,self.__check_which_bin('rm',outsarr))
			self.assertEqual(9,self.__check_which_bin('cat',outsarr))
			self.assertEqual(10,self.__check_which_bin('printf',outsarr))
			self.assertEqual(11,self.__check_which_bin('ln',outsarr))
			self.assertEqual(12,self.__check_which_bin('true',outsarr))
			self.assertEqual(13,self.__check_which_bin('touch',outsarr))
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
		s += self.__format_make_common('all:')
		s += self.__format_make_command('${ECHO} "CVALUE $(call get_value_default,${CVALUE},default_c_value)"')
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


	def test_varop_case(self):
		testf = None
		try:
			makelibdir = self.__get_makelib_dir()
			longname = make_tempfile()
			s = self.__format_varop_testmak(makelibdir,longname)
			testf = self.__write_tempfile(s)
			outsarr = self.__run_make(testf,'all')
			self.assertEqual(len(outsarr),2)
			self.assertEqual(0,self.__check_str_value(outsarr,'CVALUE default_c_value'))
			self.assertEqual(1,self.__check_str_value(outsarr,'%s shortname %s'%(longname,self.__get_shortname(longname))))
			vardict = dict()
			vardict['C'] = 'c_value_set'
			outsarr = self.__run_make(testf,'all',vardict)
			self.assertEqual(len(outsarr),2)
			self.assertEqual(0,self.__check_str_value(outsarr,'CVALUE c_value_set'))
			self.assertEqual(1,self.__check_str_value(outsarr,'%s shortname %s'%(longname,self.__get_shortname(longname))))
		finally:
			self.__remove_file_safe(testf)
			self.__remove_file_safe(longname)


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
		"$" : "*"
	}
	'''
	commandline = commandline_fmt%(os.path.dirname(os.path.realpath(__file__)))
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	set_log_level(args)
	sys.argv[1:] = args.args
	if args.reserved : 
		os.environ['TEST_RESERVED'] = '1'
	else:
		if 'TEST_RESERVED' in os.environ.keys():
			del os.environ['TEST_RESERVED']
	unittest.main(verbosity=args.verbose,failfast=args.failfast)
	return

if __name__ == '__main__':
	main()
