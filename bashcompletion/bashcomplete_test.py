#! /usr/bin/env python

import extargsparse
import unittest
import tempfile

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


class debug_bashcomlete_case(unittest.TestCase):
    def setUp(self):
        self.__tempfiles = []
        return

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

    def tearDown(self):
        if 'TEST_RESERVED' not in os.environ.keys():
            for f in self.__tempfiles:
                self.__remove_file_safe(f)

        self.__tempfiles = []
        return

    @classmethod
    def setupClass(cls):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def __write_tempfile(self,s):
    	tempf = make_tempfile()
        with open(tempf,'wb') as f:
            f.write('%s'%(s))
        self.__tempfiles.append(tempf)
        return tempf

    def test_A001(self):
    	commandline='''
		{
		    "verbose|v": "+",
		    "input|i##default (stdin)##": null,
		    "output|o##default (stdout)##": null,
		    "pattern|p": "%REPLACE_PATTERN%",
		    "bashinsert<bashinsert_handler>": {
		        "$": "*"
		    },
		    "bashstring<bashstring_handler>": {
		        "$": "*"
		    },
		    "makepython<makepython_handler>": {
		        "$": "*"
		    },
		    "makeperl<makeperl_handler>": {
		        "$": "*"
		    },
		    "shperl<shperl_handler>": {
		        "$": "*"
		    },
		    "shpython<shpython_handler>": {
		        "$": "*"
		    },
		    "pythonperl<pythonperl_handler>": {
		        "$": "*"
		    }
		}
    	'''

    	return
