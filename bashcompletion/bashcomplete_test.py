#! /usr/bin/env python

import extargsparse
import unittest
import tempfile
import os
import sys
import logging
import cmdpack

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
            if sys.version[0] == '2':
                f.write('%s'%(s))
            else:
                f.write(s.encode(encoding='UTF-8'))
        self.__tempfiles.append(tempf)
        return tempf

    def __check_completion_output(self,jsonstr,inputargs,outputlines,additioncode=None):
        tempf = self.__write_tempfile(jsonstr)
        runfile = self.__write_tempfile('')
        codef = None
        if additioncode is not None:
            codef = self.__write_tempfile(additioncode)
        # now to make format for the job
        cmds = []
        cmds.append('%s'%(sys.executable))
        curdir = os.path.realpath(os.path.dirname(__file__))
        templatefile = os.path.join(curdir,'bashcomplete_base.py')
        cmds.append(templatefile)
        cmds.append('-o')
        cmds.append(runfile)
        cmds.append('debug')
        if codef is not None:
            cmds.append(codef)
        logging.debug('format command (%s)'%(cmds))
        cmdpack.run_cmd_wait(cmds)
        logging.debug('format over')
        cmds = []
        cmds.append('%s'%(sys.executable))
        cmds.append(runfile)
        cmds.append('-i')
        cmds.append(tempf)
        cmds.append('--')
        cmds.extend(inputargs)
        logging.debug('run (%s)'%(cmds))
        idx = 0
        for l in cmdpack.run_cmd_output(cmds):
            l = l.rstrip('\r\n')
            logging.debug('[%d][%s][%d]'%(idx,l,len(outputlines)))
            self.assertTrue( idx < len(outputlines) )
            self.assertEqual(l,outputlines[idx])
            idx += 1
        self.assertEqual(idx,len(outputlines))
        return

    def __get_list_dir(self,pathext):
        retd = []
        if pathext.startswith('/'):
            basedir = os.path.dirname(pathext)
        else:
            basedir = os.path.dirname(pathext)
        if len(basedir) == 0:
            basedir = '.'
        logging.debug('cd (%s)'%(basedir))
        try:
            for l in os.listdir(basedir):
                ll = os.path.join(basedir,l)
                logging.debug('l %s pathext(%s)'%(ll,pathext))
                if ll.startswith(pathext):
                    retd.append(ll)
        except:
            pass
        logging.debug('retd (%s)'%(retd))
        return retd

    def __check_completion_output_add_files(self,jsonstr,inputargs,outputlines,pathset='',additioncode=None):
        if pathset == '':
            pathset= '.'
        outputlines.extend(self.__get_list_dir(pathset))
        logging.debug('outputlines (%s)'%(outputlines))
        self.__check_completion_output(jsonstr,inputargs,outputlines,additioncode)
        return


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
        outputlines = []
        # this is need long opt args
        outputlines.extend(['--input','--json','--output','--pattern'])
        outputlines.extend(['--help','--verbose'])
        # short flag for need args
        outputlines.extend(['-i','-o','-p'])
        # short flag for no args 
        outputlines.extend(['-h','-v'])
        # the subcommand
        outputlines.extend(['bashinsert','bashstring','makeperl','makepython','pythonperl','shperl','shpython'])
        self.__check_completion_output_add_files(commandline,['insertcode'],outputlines)
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
    commandline='''
    {
        "verbose|v" : "+",
        "failfast|f" : false,
        "reserved|r" : false,
        "$" : "*"
    }
    '''
    parser = extargsparse.ExtArgsParse(None,priority=[])
    parser.load_command_line_string(commandline)
    args = parser.parse_command_line(None,parser)
    set_log_level(args)
    if args.reserved:
        os.environ['TEST_RESERVED'] = '1'
    else:
        if 'TEST_RESERVED' in os.environ.keys():
            del os.environ['TEST_RESERVED']
    newargs = []
    if args.verbose > 0:
        vflags = '-'
        vflags += 'v' * args.verbose
        newargs.append(vflags)
    if args.failfast:
        newargs.append('--failfast')
    newargs.extend(args.args)
    sys.argv[1:]=newargs
    unittest.main()
    return

if __name__ == '__main__':
    main()