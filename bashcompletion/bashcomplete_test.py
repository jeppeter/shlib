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
        return

    def tearDown(self):
        return

    @classmethod
    def setupClass(cls):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def __write_tempfile(self,s):
    	tempf = make_tempfile()

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
