#! /usr/bin/env python

import extargsparse
import unittest
import tempfile
import os
import sys
import logging
import cmdpack
import re
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

def get_full_trace_back(trback,tabs=1,cnt=0):
    s = ''
    frm = getattr(trback,'tb_frame',None)
    if frm is not None:
        code = getattr(frm,'f_code',None)
        if code is not None:
            s += ' ' * tabs * 4
            s += '[%d][%s:%s:%s]\n'%(cnt,code.co_filename,code.co_name,frm.f_lineno)
            ntrace = getattr(trback,'tb_next',None)
            if ntrace is not None:
                s += get_full_trace_back(ntrace,tabs,cnt+1)
    return s


def change_shell_special_dir(d):
    retd = d
    try:
        devnullfd = open(os.devnull,'w')
        p = subprocess.Popen(['/bin/bash'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=devnullfd,shell=False)
        p.stdin.write('export DIRVALUE=%s\n'%(d))
        p.stdin.write('echo -n "$DIRVALUE"\n')
        p.stdin.close()
        lines = p.stdout.readlines()
        for l in lines:
            l = l.rstrip('\r\n')
            retd = l
            logging.info('[%s] [%s]'%(d,retd))
        p = None
        if devnullfd is not None:
            devnullfd.close()
        devnullfd = None
    except:
        trback = sys.exc_info()[2]
        exceptname = sys.exc_info()[1]
        s = ''
        s += 'exception %s:\n'%(exceptname)
        s +='trace back:\n'
        s += get_full_trace_back(trback,1,0)
        logging.warn('%s'%(s))
        retd = d
    return retd



class debug_bashcomplete_case(unittest.TestCase):
    def setUp(self):
        self.__tempfiles = []
        self.__resultok = False
        self.__verbose = 0
        if 'TEST_VERBOSE' in os.environ.keys():
            self.__verbose = int(os.environ['TEST_VERBOSE'])
        return

    def __remove_dir(self,dirn,issuper=False):
        if issuper:
            cmd = ['sudo','rm','-rf',dirn]
        else:
            cmd = ['rm','-rf',dirn]
        subprocess.check_call(cmd)
        return

    def __quote_string(self,s):
        rets = ''
        for c in s:
            if c == '"':
                rets += '\\"'
            elif c == '\\':
                rets += '\\\\'
            else:
                rets += c
        return rets


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
        if 'TEST_RESERVED' not in os.environ.keys() and self.__resultok :
            for f in self.__tempfiles :
                self.__remove_file_safe(f)

        self.__tempfiles = []
        return

    @classmethod
    def setupClass(cls):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def __write_tempfile(self,s,infile=None):
        if infile is None:
            tempf = make_tempfile()
            self.__tempfiles.append(tempf)
        else:
            tempf = infile
        with open(tempf,'wb') as f:
            if sys.version[0] == '2':
                f.write('%s'%(s))
            else:
                f.write(s.encode(encoding='UTF-8'))
        logging.debug('write (%s) [%s]'%(s,tempf))
        return tempf

    def __write_basic_files(self,jsonstr,prefix,additioncode=None,outfile=None,extoptions=None):
        jsonfile = self.__write_tempfile(jsonstr)
        runfile = self.__write_tempfile('')
        codef = None
        optfile = None
        if additioncode is not None:
            codef = self.__write_tempfile(additioncode)
        if extoptions is not None:
            optfile = self.__write_tempfile(extoptions)
        # now to make format for the job
        cmds = []
        cmds.append('%s'%(sys.executable))
        curdir = os.path.realpath(os.path.dirname(__file__))
        if outfile is None:
            pythonfile = os.path.join(curdir,'bashcomplete_format_debug.py')
            templatefile = os.path.join(curdir,'bashcomplete.py.tmpl')
        else:
            pythonfile = outfile
            templatefile = os.path.join(curdir,'bashcomplete.py.tmpl')
        cmds.append(pythonfile)
        if templatefile is not None:
            cmds.append('--basefile')
            cmds.append(templatefile)
        if jsonfile is not None:
            cmds.append('--jsonfile')
            cmds.append(jsonfile)
        if self.__verbose > 0:
            verbosemode = '-'
            verbosemode += 'v' * self.__verbose
            cmds.append(verbosemode)
        cmds.append('--output')
        cmds.append(runfile)
        cmds.append('--prefix')
        cmds.append(prefix)
        if optfile is not None:
            cmds.append('--optfile')
            cmds.append(optfile)
        cmds.append('debug')
        if codef is not None:
            cmds.append(codef)
        logging.debug('format command (%s)'%(cmds))
        noout = 1
        if self.__verbose >= 3:
            noout = 0
        cmdpack.run_cmd_wait(cmds,mustsucc=1,noout=noout,shellmode=True)
        return jsonfile,runfile,templatefile,codef,optfile

    def __check_completion_output(self,jsonstr,inputargs,outputlines,additioncode=None,outfile=None,extoptions=None,index=None,line=None):
        prefix = 'prog'
        if len(inputargs) > 0:
            prefix = os.path.basename(inputargs[0])
            prefix = prefix.replace('\.','_')
        jsonfile,runfile,templatefile,codef,optfile = self.__write_basic_files(jsonstr,prefix,additioncode,outfile,extoptions)
        if line is None:
            line = ''
            for c in inputargs:
                if len(line) > 0:
                    line += ' '
                line += '"%s"'%(c)
        if index is None:
            index = len(line)
        cmds = []
        cmds.append('%s'%(sys.executable))
        cmds.append(runfile)
        cmds.append('-i')
        cmds.append(jsonfile)
        if optfile is not None:
            cmds.append('--optfile')
            cmds.append(optfile)
        if self.__verbose >= 3:
            cmds.append('--debugmode')
        if self.__verbose > 0:
            verbosemode = '-'
            verbosemode += 'v' * self.__verbose
            cmds.append(verbosemode)
        if jsonfile is not None:
            cmds.append('--jsonfile')
            cmds.append(jsonfile)
        cmds.append('--line')
        cmds.append(line)
        cmds.append('--index')
        cmds.append('%s'%(index))
        cmds.append('complete')
        cmds.append('--')
        cmds.extend(inputargs)
        logging.debug('run (%s)'%(cmds))
        idx = 0
        stderrout = False
        if self.__verbose >= 3:
            stderrout = None
        for l in cmdpack.run_cmd_output(cmds,True,stderrout):
            l = l.rstrip('\r\n')
            logging.debug('[%d]l [%s]'%(idx,l))
            self.assertTrue( idx < len(outputlines))
            logging.debug('[%d][%s] [%s]'%(idx,l,outputlines[idx].rstrip('\r\n')))
            self.assertEqual(l,outputlines[idx])
            idx += 1
        self.assertEqual(idx,len(outputlines))
        return

    def __get_list_dir(self,pathext,endwords='',extoptions=None):
        retd = []
        options = extargsparse.ExtArgsOptions(extoptions)
        if options.endwordshandle is None:
            options.endwordshandle = False
        basedir = os.path.dirname(pathext)
        if len(basedir) == 0:
            if len(pathext) == 0:
                basedir = '.'
                appenddir = ''
            else:
                appenddir = pathext
                basedir = pathext
                basedir = change_shell_special_dir(basedir)
        else:
            appenddir = basedir
            basedir = change_shell_special_dir(basedir)

        logging.debug('cd (%s)'%(basedir))
        try:
            for l in os.listdir(basedir):
                if len(appenddir) == 0:
                    ll = l
                else:
                    ll = os.path.join(appenddir,l)
                logging.debug('l %s pathext(%s)'%(ll,pathext))
                if ll.startswith(pathext):
                    if options.endwordshandle and ll.endswith(endwords):
                        retd.append(re.sub('%s$'%(endwords),'',ll))
                    elif not options.endwordshandle:
                        retd.append(ll)
        except:
            pass
        retd = sorted(retd)
        logging.debug('retd (%s)'%(retd))
        return retd

    def __check_completion_output_add_files(self,jsonstr,inputargs,outputlines,pathset='',additioncode=None,outfile=None,extoptions=None,index=None,line=None):
        outputlines.extend(self.__get_list_dir(pathset))
        logging.debug('outputlines (%s)'%(outputlines))
        self.__check_completion_output(jsonstr,inputargs,outputlines,additioncode,outfile,extoptions,index,line)
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
        outputlines.extend(['--help','--input','--json','--output','--pattern','--verbose'])
        outputlines.extend(['-h','-i','-o','-p','-v'])
        outputlines.extend(['bashinsert','bashstring','makeperl','makepython','pythonperl','shperl','shpython'])
        self.__check_completion_output_add_files(commandline,['insertcode'],outputlines)
        outputlines = []
        # this is need long opt args
        outputlines.extend(['--help','--input','--json','--output','--pattern','--verbose'])
        outputlines.extend(['-h','-i','-o','-p','-v'])
        outputlines.extend(['bashinsert','bashstring','makeperl','makepython','pythonperl','shperl','shpython'])
        self.__check_completion_output_add_files(commandline,['insertcode',''],outputlines)
        self.__resultok = True
        return

    def test_A002(self):
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
        outputlines.extend(['--help','--input','--json','--output','--pattern','--verbose'])
        # short flag for need args
        outputlines.extend(['-h','-i','-o','-p','-v'])
        # to make the command
        self.__check_completion_output(commandline,['insertcode','-'],outputlines)
        self.__resultok = True
        return

    def test_A003(self):
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
        self.__check_completion_output_add_files(commandline,['insertcode','~'],outputlines,'~')
        self.__resultok = True
        return

    def test_A004(self):
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
        outputlines.extend(['makeperl','makepython'])
        self.__check_completion_output_add_files(commandline,['insertcode','make'],outputlines,'make')
        self.__resultok = True
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
    if logging.root is not None and len(logging.root.handlers) > 0:
        logging.root.handlers = []
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
    os.environ['TEST_VERBOSE'] = '%d'%(args.verbose)
    if args.reserved:
        os.environ['TEST_RESERVED'] = '1'
    else:
        if 'TEST_RESERVED' in os.environ.keys():
            del os.environ['TEST_RESERVED']
    newargs = []
    newargs.extend(args.args)
    sys.argv[1:]=newargs
    unittest.main(verbosity=args.verbose,failfast=args.failfast)
    return

if __name__ == '__main__':
    main()