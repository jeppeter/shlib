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
import random
import time
try:
    import pexpect
    pexpectimported=True
except:
    pexpectimported=False

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
    if not isinstance(s,str):
        logging.warning('[%s] not str'%(s))
    return s

def read_file(infile=None):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')
    bmode = False
    if 'b' in fin.mode:
        bmode = True
    for l in fin:
        if sys.version[0] == '2' or not bmode:
            s += l
        else:
            s += l.decode(encoding='UTF-8')
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s


def encode_string_mode(instr,bmode):
    retstr = instr
    if sys.version[0] != '2' and bmode:
        retstr = instr.encode(encoding='UTF-8')
    return retstr

def encode_eval_string(instr):
    rets = ''
    for c in instr:
        if c == '`':
            rets += '\\`'
        elif c == '"':
            rets += '\\"'
        else:
            rets += c
    return rets

def change_shell_special_dir(d):
    retd = d
    devnullfd = None
    logging.info('d [%s]'%(d))
    try:
        #devnullfd = open(os.devnull,'w')
        p = subprocess.Popen(['/bin/bash'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=devnullfd,shell=False)
        bmode = False
        if 'b' in p.stdin.mode:
            bmode = True
        curdir = os.getcwd()
        # to make the current directory
        p.stdin.write(encode_string_mode('cd %s\n'%(curdir),bmode))
        cmd = 'export DIRVALUE=`%s '%(sys.executable)
        cmd += '-c "import os;import sys;print(\'%s\'%(os.path.expanduser(sys.argv[1])))"'
        cmd += ' "%s"`'%(encode_eval_string(d))
        cmd += '\n'
        logging.info('cmd [%s]'%(cmd))
        p.stdin.write(encode_string_mode(cmd,bmode))
        p.stdin.write(encode_string_mode('echo -n "$DIRVALUE"\n',bmode))
        p.stdin.close()
        p.stdin = None
        lines = p.stdout.readlines()
        p.stdout.close()
        p.stdout = None
        for l in lines:
            if sys.version[0] != '2':
                l = l.decode(encoding='UTF-8')
            l = l.rstrip('\r\n')
            retd = l
            logging.info('[%s] [%s]'%(d,retd))
        p = None
    except:
        trback = sys.exc_info()[2]
        exceptname = sys.exc_info()[1]
        s = ''
        s += 'exception %s:\n'%(exceptname)
        s +='trace back:\n'
        s += get_full_trace_back(trback,1,0)
        logging.warning('%s'%(s))
        retd = d
    finally:
        if devnullfd is not None:
            devnullfd.close()
        devnullfd = None
    return retd

def regular_quote(ins):
    regular_special_case = ['+','*','(',')','[',']','-','?','\\','^','$','{','}']
    rets = ''
    for c in ins:
        if c in regular_special_case:
            rets += '\\'
        rets += c
    return rets


KEY_UP = '\x1b[A'
KEY_DOWN = '\x1b[B'
KEY_RIGHT = '\x1b[C'
KEY_LEFT = '\x1b[D'


class ExpLogObject(object):
    def __init__(self,logfd=None,note='read'):
        self.__logfd= None
        self.__bmode = False
        self.__note=note
        if logfd is not None:
            self.__logfd = logfd
            self.__bmode = False
            if 'b' in self.__logfd.mode:
                self.__bmode = True
        return

    def write(self,s):
        bmode = False
        if isinstance(s,bytes):
            bmode = True
        if self.__bmode == bmode or sys.version[0] == '2':
            self.__logfd.write(s)
        elif self.__bmode :
            # we encode
            self.__logfd.write(s.encode(encoding='UTF-8'))
        elif bmode:
            self.__logfd.write(s.decode(encoding='UTF-8'))
        return

    def flush(self):
        if self.__logfd is not None:
            self.__logfd.flush()
        return

def read_buffer(child,timeout=.3,checkfunc=None,checkctx=None,bufsize=1024):
    if sys.version[0] == '2':
        totalbuf = ''
    else:
        totalbuf = b''
    while True:
        try:
            cbuf = child.read_nonblocking(bufsize,timeout=timeout)
        except pexpect.exceptions.TIMEOUT as e:
            break
        totalbuf += cbuf
        if checkfunc is not None:
            bret = checkfunc(totalbuf,checkctx)
            if bret :
                break
    retbuf = totalbuf
    if sys.version[0] != '2':
        retbuf = totalbuf.decode(encoding='UTF-8')
    return retbuf

def get_read_completion(child,timeout=0.5):
    totalbuf = ''
    requireexpr = re.compile('.*\(y or n\)$',re.M | re.S)
    moreexpr = re.compile('.*--More--$',re.M | re.S)
    handlemode = None
    while True:
        cbuf = read_buffer(child,timeout=timeout)
        handlemode = None
        sarr = re.split('\n',cbuf)
        for l in sarr:
            l = l.rstrip('\r\n')
            if l.startswith('>>>>>>'):
                continue
            if requireexpr.match(l):
                assert(handlemode is None)
                handlemode = 'yeshandle'
            elif moreexpr.match(l):
                assert(handlemode is None)
                handlemode = 'more'
            else:
                l = l.replace('\r','')
                # replace bell
                l = l.replace('\x07','')
                # that is the erase line
                l = l.replace('\x1b[K','')
                if len(l) > 0:
                    totalbuf += '%s\n'%(l)
        if handlemode is not None:
            if handlemode == 'yeshandle':
                child.send('y')
            elif handlemode == 'more' :
                child.send('y')
        else:
            break
    return totalbuf

RANDOM_LOWER = 'abcdefghijklmnopqrstuvwxyz'
RANDOM_UPPER = RANDOM_LOWER.upper()
RANDOM_NUMBER = '0123456789'
RANDOM_ALPHBET = RANDOM_LOWER + RANDOM_UPPER
RANDOM_CHARS = RANDOM_ALPHBET + RANDOM_NUMBER + '_'

def get_temp_value(numchars=10):
    newargspattern = ''
    while len(newargspattern) < numchars:
        if len(newargspattern) == 0:
            newargspattern += random.choice(RANDOM_ALPHBET)
        else:
            newargspattern += random.choice(RANDOM_CHARS)
    return newargspattern


class ValueAttr(object):
    def __init__(self):
        self.__obj = dict()
        self.__access = dict()
        return

    def __setattr__(self,key,val):
        if not key.startswith('_'):
            self.__obj[key] = val
            self.__access[key] = True
            return
        self.__dict__[key] = val
        return

    def __getattr__(self,key):
        if not key.startswith('_'):
            if key in self.__obj.keys():
                return self.__obj[key]
            return None
        return self.__dict__[key]

    def __str__(self):
        s = '{'
        for k in self.__obj.keys():
            s += '%s=%s;'%(k,self.__obj[k])
        s += '}'
        return s

    def __repr__(self):
        return self.__str__()

    def __has_accessed(self,name):
        if name in self.__access.keys():
            return True
        return False

    def is_accessed(self,name):
        return self.__has_accessed(name)

    def get_keys(self):
        return self.__obj.keys()


class debug_bashcomplete_case(unittest.TestCase):
    def setUp(self):
        self.__tempfiles = []
        self.__resultok = False
        self.__verbose = 0
        self.__infomsg = None
        self.__infomsg = extargsparse.ExtArgsParse()
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

    def __write_basic_files(self,cmdact,jsonstr,prefix,additioncode=None,outfile=None,extoptions=None,relasemode=None):
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
            if relasemode is None:                
                pythonfile = os.path.join(curdir,'bashcomplete_format_debug.py')
                templatefile = os.path.join(curdir,'bashcomplete.py.tmpl')
            else:
                logging.info('release mode')
                pythonfile = os.path.join(curdir,'bashcomplete_format')
                templatefile = None
        else:
            if relasemode is None:
                pythonfile = outfile
                templatefile = os.path.join(curdir,'bashcomplete.py.tmpl')
            else:
                logging.info('release mode')
                pythonfile = outfile
                templatefile = None
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
        cmds.append(cmdact)
        if codef is not None:
            cmds.append(codef)
        logging.debug('format command (%s)'%(cmds))
        noout = 1
        if self.__verbose >= 3:
            noout = 0
        cmdpack.run_cmd_wait(cmds,mustsucc=1,noout=noout,shellmode=True)
        return jsonfile,runfile,templatefile,codef,optfile

    def __check_completion_output(self,jsonstr,inputargs,outputlines,valattr=None):
        prefix = 'prog'
        if len(inputargs) > 0:
            prefix = os.path.basename(inputargs[0])
            prefix = prefix.replace('\.','_')
        if valattr is None:
            valattr = ValueAttr()
        jsonfile,runfile,templatefile,codef,optfile = self.__write_basic_files('debug',jsonstr,prefix,valattr.additioncode,valattr.outfile,valattr.extoptions,valattr.releasemode)
        line = valattr.line
        if line is None:
            line = ''
            idx = 0
            for c in inputargs:
                if len(line) > 0:
                    line += ' '
                if self.__must_quote_string(c):
                    line += '"%s"'%(c)
                else:
                    line += c
                idx += 1
        index = valattr.index
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
        logging.info('cmds (%s)'%(cmds))
        for l in cmdpack.run_cmd_output(cmds,True,stderrout):
            l = l.rstrip('\r\n')
            logging.debug('[%d]l [%s]'%(idx,l))
            self.assertTrue( idx < len(outputlines))
            logging.debug('[%d][%s] [%s]'%(idx,l,outputlines[idx].rstrip('\r\n')))
            self.assertEqual(l,outputlines[idx])
            idx += 1
        self.assertEqual(idx,len(outputlines))
        return

    def __start_pexpect(self,sourcefile,timeout=0.5):
        child = pexpect.spawn('/bin/bash')
        # now we should make sure 
        logobj = None
        if self.__verbose >= 3:
            logobj = ExpLogObject(sys.stderr)
        child.logfile = logobj
        child.send('export PS1=\'>>>>>>\'\r\n')
        child.expect('>>>>>>',timeout=timeout)
        curdir = os.getcwd()
        # to change the current directory
        child.send('cd "%s"\r\n'%(self.__quote_string(curdir)))
        child.expect('"%s"'%(self.__quote_string(curdir)),timeout=timeout)
        child.expect('>>>>>>',timeout=timeout)
        child.send('source %s\r\n'%(sourcefile))
        child.expect('%s\r\n'%(sourcefile),timeout=timeout)
        child.expect('>>>>>>',timeout=timeout)
        return child

    def __check_line_in_completion(self,l,sarr):
        for sl in sarr:
            chgs = sl.replace(l,'')
            if chgs != sl:
                reorigin = regular_quote(l)
                respaces = re.compile('.*\s+%s\s+.*'%(reorigin),re.S)
                rewithstart=re.compile('^%s\s+.*'%(reorigin),re.S)
                reendwith = re.compile('.*\s+%s$'%(reorigin),re.S)
                reonly = re.compile('^%s$'%(reorigin))
                logging.info('l[%s]reorigin [%s]'%(l,reorigin))
                if respaces.match(sl) or rewithstart.match(sl) or \
                    reendwith.match(sl) or reonly.match(sl):
                    return True
        logging.error('%s not in (%s)'%(l,sarr))
        return False

    def __check_line_in_outlines(self,l,sarr):
        startidx =0 
        while startidx < len(l) and (l[startidx] == ' ' or l[startidx] == '\t'):
            startidx += 1
        endidx = startidx + 1
        if endidx >= len(l):
            # nothing to match
            return True

        while startidx < len(l):
            partl = l[startidx:endidx]
            finds = []
            for s in sarr:
                if s.startswith(partl):
                    finds.append(s)
            if len(finds) == 0:
                logging.error('can not find [%s] in (%s)'%(l,sarr))
                return False
            while endidx < len(l):
                partl = l[startidx:endidx]
                okfind = False
                for s in finds:
                    if s.startswith(partl):
                        okfind = True
                if okfind:
                    endidx += 1
                else:
                    endidx -= 1
                    partl = l[startidx:endidx]
                    okfind = False
                    for s in finds:
                        if partl == s:
                            okfind = True
                            break
                    if okfind:
                        break
                    else:
                        logging.error('can not find [%s] in (%s)'%(l,sarr))
                        return False
            # now we should find it
            startidx = endidx + 1
            while startidx < len(l) and (l[startidx] == ' ' or l[startidx] == '\t'):
                startidx += 1
            endidx = startidx + 1
            if endidx >= len(l):
                return True
        logging.error('can not find [%s] in (%s)'%(l,sarr))
        return False

    def __must_quote_string(self,c):
        if ' ' in c:
            return True
        if '\t' in c:
            return True
        return False

    def __expect_bash_supported(self):
        plat = sys.platform.lower()
        if not pexpectimported:
            logging.error('no pexpect imported')
            return False
        if plat == 'win32':
            logging.error('win32 not supported')
            return False
        return True

    def __remove_related_environ(self,inputarg0):
        envkeys = []
        envkeys.append('%s_COMPLETION_DEBUG_MODE'%(inputarg0.upper()))
        envkeys.append('%s_COMMAND_JSON_EXTOPTIONS'%(inputarg0.upper()))
        envkeys.append('%s_PYTHON_COMPLETE_STR'%(inputarg0.upper()))
        envkeys.append('%s_COMPLETE_VERSION'%(inputarg0.upper()))
        envkeys.append('%s_COMMAND_JSON_EXTOPTIONS'%(inputarg0.upper()))
        removkeys = []
        for k in os.environ.keys():
            if k in envkeys:
                removkeys.append(k)
        for k in removkeys:
            try:
                del os.environ[k]
            except:
                logging.warning('can not remove [%s]'%(k))
        return


    def __check_bash_completion_output(self,jsonstr,inputargs,outputlines,valattr=None):
        bret = self.__expect_bash_supported()
        if not bret:
            # nothing to handle
            return
        self.__debug_list(outputlines,'outputlines')
        prefix = 'prog'
        if valattr is None:
            valattr = ValueAttr()
        if len(inputargs) > 0:
            prefix = os.path.basename(inputargs[0])
            prefix = prefix.replace('\.','_')
        jsonfile,runfile,templatefile,codef,optfile = self.__write_basic_files('output',jsonstr,prefix,valattr.additioncode,valattr.outfile,valattr.extoptions,valattr.releasemode)
        line = valattr.line
        if line is None:
            line = ''
            idx = 0
            for c in inputargs:
                if len(line) > 0:
                    line += ' '
                if self.__must_quote_string(c):
                    line += '"%s"'%(c)
                else:
                    line += c
                idx += 1
            if idx == 1:
                # we add one in the last
                line += ' '
        index = valattr.index
        self.__debug_list(outputlines,'outputlines')
        exptimeout = valattr.timeout
        if exptimeout is None:
            exptimeout = 0.3
        if index is None:
            index = len(line) 
        self.__remove_related_environ(inputargs[0])
        logging.info('outputlines (%s)'%(outputlines))
        child = self.__start_pexpect(runfile,timeout=exptimeout)
        logging.info('line[%s]'%(line))
        child.send('%s'%(line))
        child.expect('%s'%(line),timeout=exptimeout)
        if index < len(line):
            cnt = (len(line) - index)
            child.send(KEY_LEFT * cnt)
        tabtimes = valattr.tabtimes
        if tabtimes is None:
            tabtimes = 1
        curtime = 0
        self.__debug_list(outputlines,'outputlines')
        while curtime < tabtimes:
            child.send('\t')
            time.sleep(0.1)
            child.send('\t')
            readbuf = get_read_completion(child,timeout=exptimeout)
            curtime += 1
        child.close()
        child.wait()
        logging.debug('get [%s]'%(readbuf))
        sarr = []
        for l in re.split('\n',readbuf):
            l  = l.rstrip('\r\n')
            if len(l) == 0:
                continue
            sarr.append(l)
        self.__debug_list(outputlines,'outputlines')
        idx = 0
        for l in outputlines:
            logging.info('[%d][%s]'%(idx,l))
            bret = self.__check_line_in_completion(l,sarr)
            self.assertEqual(bret,True)
            idx += 1

        for l in sarr:
            bret = self.__check_line_in_outlines(l,outputlines)
            self.assertEqual(bret,True)
        return

    def __debug_list(self,sarr,note=''):
        idx = 0
        msg = self.__infomsg.format_call_msg('',2)
        for l in sarr:
            logging.info('%s%s[%s][%s]'%(msg,note,idx,l))
            idx += 1
        return

    def __get_list_dir(self,pathext,endwords='',extoptions=None,bashmode=False):
        retd = []
        options = extargsparse.ExtArgsOptions(extoptions)
        if options.endwordshandle is None:
            options.endwordshandle = False
        basedir = os.path.dirname(pathext)
        specialhandle = False
        if len(basedir) == 0:
            basedir = change_shell_special_dir(pathext)
            if basedir == pathext:
                basedir = '.'
                appenddir = ''
            else:
                appenddir = pathext
                while len(appenddir) > 0 and appenddir[-1] == os.path.sep:
                    appenddir = appenddir[:-2]
                specialhandle = True
        else:
            appenddir = basedir
            basedir = change_shell_special_dir(basedir)

        logging.debug('cd (%s)'%(basedir))
        try:
            for l in os.listdir(basedir):
                curfile = os.path.join(basedir,l)
                if len(appenddir) == 0:
                    ll = l
                elif specialhandle:
                    ll = '%s%c%s'%(appenddir,os.path.sep,l)
                else:
                    ll = os.path.join(appenddir,l)
                if bashmode:
                    if os.path.isdir(curfile):
                        ll += os.path.sep
                logging.debug('l %s pathext(%s)'%(ll,pathext))
                if ll.startswith(pathext):
                    if options.endwordshandle and ll.endswith(endwords):
                        curf = re.sub('%s$'%(endwords),'',ll)
                        logging.info('append [%s]'%(curf))
                        retd.append(curf)
                    elif not options.endwordshandle:
                        logging.info('append [%s]'%(ll))
                        retd.append(ll)
        except:
            pass
        retd = sorted(retd)        
        self.__debug_list(retd,'retd')
        logging.debug('retd (%s)'%(retd))
        return retd

    def __check_completion_output_add_files(self,jsonstr,inputargs,outputlines,pathset='',valattr=None):
        outputlines.extend(self.__get_list_dir(pathset))
        self.__check_completion_output(jsonstr,inputargs,outputlines,valattr)
        return

    def __check_bash_completion_output_add_files(self,jsonstr,inputargs,outputlines,pathset='',valattr=None):
        outputlines.extend(self.__get_list_dir(pathset,bashmode=True))
        self.__check_bash_completion_output(jsonstr,inputargs,outputlines,valattr)
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
        valattr =ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        self.__check_completion_output_add_files(commandline,['insertcode'],outputlines,'',valattr)
        outputlines = []
        # this is need long opt args
        outputlines.extend(['--help','--input','--json','--output','--pattern','--verbose'])
        outputlines.extend(['-h','-i','-o','-p','-v'])
        outputlines.extend(['bashinsert','bashstring','makeperl','makepython','pythonperl','shperl','shpython'])
        valattr =ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        self.__check_bash_completion_output_add_files(commandline,['insertcode'],outputlines,'',valattr)
        outputlines = []
        # this is need long opt args
        outputlines.extend(['--help','--input','--json','--output','--pattern','--verbose'])
        outputlines.extend(['-h','-i','-o','-p','-v'])
        outputlines.extend(['bashinsert','bashstring','makeperl','makepython','pythonperl','shperl','shpython'])
        valattr =ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        self.__check_completion_output_add_files(commandline,['insertcode',''],outputlines,'',valattr)
        outputlines = []
        # this is need long opt args
        outputlines.extend(['--help','--input','--json','--output','--pattern','--verbose'])
        outputlines.extend(['-h','-i','-o','-p','-v'])
        outputlines.extend(['bashinsert','bashstring','makeperl','makepython','pythonperl','shperl','shpython'])
        valattr =ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        self.__check_bash_completion_output_add_files(commandline,['insertcode',''],outputlines,'',valattr)
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
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        self.__check_completion_output(commandline,['insertcode','-'],outputlines,valattr)
        self.__check_bash_completion_output(commandline,['insertcode','-'],outputlines,valattr)
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
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        self.__check_completion_output_add_files(commandline,['insertcode','~'],outputlines,'~',valattr)
        outputlines = []
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        # in the 
        retd = self.__get_list_dir('~',bashmode=True)
        for l in retd:
            outputlines.append(re.sub('^~/','',l))
        self.__check_bash_completion_output(commandline,['insertcode','~'],outputlines,valattr)
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
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        self.__check_completion_output_add_files(commandline,['insertcode','make'],outputlines,'make',valattr)
        outputlines = []
        outputlines.extend(['makeperl','makepython'])
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        self.__check_bash_completion_output_add_files(commandline,['insertcode','make'],outputlines,'make',valattr)
        self.__resultok = True
        return

    def test_A005(self):
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
        valattr = ValueAttr()
        valattr.line = 'insertcode make'
        valattr.index = 13
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        self.__check_completion_output_add_files(commandline,['insertcode','make'],outputlines,'make',valattr)
        outputlines = []
        outputlines.extend(['makeperl','makepython'])
        valattr = ValueAttr()
        valattr.line = 'insertcode make'
        valattr.index = 13
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        self.__check_bash_completion_output_add_files(commandline,['insertcode','make'],outputlines,'mak',valattr)
        self.__resultok = True
        return

    def test_A006(self):
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
        outputlines.extend(['--help','--input','--json','--output','--pattern'])
        outputlines.extend(['-h','-i','-o','-p'])
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        self.__check_completion_output(commandline,['insertcode','--verbose','-'],outputlines,valattr)
        self.__check_bash_completion_output(commandline,['insertcode','--verbose','-'],outputlines,valattr)
        self.__resultok = True
        return

    def test_A007(self):
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
        outputlines.extend(['--help','--input','--json','--output','--pattern'])
        outputlines.extend(['-h','-i','-o','-p'])
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        self.__check_completion_output(commandline,['insertcode','--verbose','-v','-'],outputlines,valattr)
        self.__check_bash_completion_output(commandline,['insertcode','--verbose','-v','-'],outputlines,valattr)
        self.__resultok = True
        return

    def test_A008(self):
        commandline='''
        {
            "verbose|v" : "+",
            "jsonstr|j##jsonstr to read  none read from input or stdin##" : null,
            "basefile|B" : null,
            "jsonfile" : null,
            "optfile|F" : null,
            "extoptions|E" : null,
            "input|i" : null,
            "output|o" : null,
            "prefix|p" : null,
            "output<output_handler>" : {
                "$" : "*"
            },
            "release<release_handler>" : {
                "$" : "*"
            },
            "debug<debug_handler>" : {
                "$" : "*"
            },
            "verify<verify_handler>" : {
                "$" : 0
            },
            "version<version_handler>" : {
                "$" : 0
            },
            "selfcomp<selfcomp_handler>" : {
                "$" : 0
            }
        }        
        '''
        outputlines = []
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        self.__check_completion_output_add_files(commandline,['bashcomplete_format','-o','ba'],outputlines,'ba',valattr)
        self.__check_bash_completion_output_add_files(commandline,['bashcomplete_format','-o','ba'],outputlines,'ba',valattr)
        self.__resultok = True
        return

    def test_A009(self):
        commandline='''
        {
            "verbose|v" : "+",
            "jsonstr|j##jsonstr to read  none read from input or stdin##" : null,
            "basefile|B" : null,
            "jsonfile" : null,
            "optfile|F" : null,
            "extoptions|E" : null,
            "input|i" : null,
            "output|o" : null,
            "prefix|p" : null,
            "output<output_handler>" : {
                "$" : "*"
            },
            "release<release_handler>" : {
                "$" : "*"
            },
            "debug<debug_handler>" : {
                "$" : "*"
            },
            "verify<verify_handler>" : {
                "$" : 0
            },
            "version<version_handler>" : {
                "$" : 0
            },
            "selfcomp<selfcomp_handler>" : {
                "$" : 0
            }
        }        
        '''
        outputlines = []
        outputlines.extend(['--optfile','--output'])
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        self.__check_completion_output_add_files(commandline,['bashcomplete_format','--jsonfile','test.json','--o'],outputlines,'--o',valattr)
        self.__check_bash_completion_output_add_files(commandline,['bashcomplete_format','--jsonfile','test.json','--o'],outputlines,'--o',valattr)
        self.__resultok = True
        return

    def test_A010(self):
        commandline='''
        {
            "verbose|v" : "+",
            "jsonstr|j##jsonstr to read  none read from input or stdin##" : null,
            "basefile|B" : null,
            "jsonfile" : null,
            "optfile|F" : null,
            "extoptions|E" : null,
            "input|i" : null,
            "output|o" : null,
            "prefix|p" : null,
            "output<output_handler>" : {
                "$" : "*"
            },
            "release<release_handler>" : {
                "$" : "*"
            },
            "debug<debug_handler>" : {
                "$" : "*"
            },
            "verify<verify_handler>" : {
                "$" : 0
            },
            "version<version_handler>" : {
                "$" : 0
            },
            "selfcomp<selfcomp_handler>" : {
                "$" : 0
            }
        }        
        '''
        outputlines = []
        outputlines.extend(['--basefile','--extoptions','--help','--input','--json','--jsonfile','--jsonstr'])
        outputlines.extend(['--optfile','--prefix','--selfcomp-json','--verbose'])
        outputlines.extend(['-B','-E','-F','-h','-i','-j','-p','-v'])
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        valattr.line = 'bashcomplete_format -o bashcomplete_format.completion  selfcomp '
        valattr.index = 64
        self.__check_completion_output_add_files(commandline,['bashcomplete_format','-o','bashcomplete_format.completion','selfcomp'],outputlines,'',valattr)
        outputlines = []
        outputlines.extend(['--basefile','--extoptions','--help','--input','--json','--jsonfile','--jsonstr'])
        outputlines.extend(['--optfile','--prefix','--selfcomp-json','--verbose'])
        outputlines.extend(['-B','-E','-F','-h','-i','-j','-p','-v'])
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.tabtimes = 2
        valattr.line = 'bashcomplete_format -o bashcomplete_format.completion  selfcomp '
        valattr.index = 64
        self.__check_bash_completion_output_add_files(commandline,['bashcomplete_format','-o','bashcomplete_format.completion','selfcomp'],outputlines,'',valattr)
        self.__resultok = True
        return

    def test_A011(self):
        commandline='''
        {
            "verbose|v" : "+",
            "jsonstr|j##jsonstr to read  none read from input or stdin##" : null,
            "basefile|B" : null,
            "jsonfile" : null,
            "optfile|F" : null,
            "extoptions|E" : null,
            "input|i" : null,
            "output|o" : null,
            "prefix|p" : null,
            "output<output_handler>" : {
                "$" : "*"
            },
            "release<release_handler>" : {
                "$" : "*"
            },
            "debug<debug_handler>" : {
                "$" : "*"
            },
            "verify<verify_handler>" : {
                "$" : 0
            },
            "version<version_handler>" : {
                "$" : 0
            },
            "selfcomp<selfcomp_handler>" : {
                "$" : 0
            }
        }        
        '''
        outputlines = []
        _tempfile = None
        while True:
            _tempfile = get_temp_value(12)
            if _tempfile not in os.listdir(os.getcwd()):
                break

        _newtempfile = None
        while True:
            _newtempfile = None
            _newtempfile = _tempfile
            # we add space in the name
            _newtempfile += ' '
            _newtempfile += get_temp_value(12)
            if _newtempfile not in os.listdir(os.getcwd()):
                break
        # we make sure this file is ok
        self.__write_tempfile('',_newtempfile)
        self.__tempfiles.append(_newtempfile)
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.line = 'bashcomplete_format -o \'%s '%(_tempfile)
        valattr.index = len(valattr.line)
        outputlines.append(_newtempfile)
        self.__check_completion_output(commandline,['bashcomplete_format','-o','%s '%(_tempfile)],outputlines,valattr)
        outputlines.remove(_newtempfile)
        # for the handling ,we should make it for the next
        _val = _newtempfile.replace('%s '%(_tempfile),'')
        # this is the endof line
        _val += '\' '
        outputlines.append(_val)
        self.__check_bash_completion_output(commandline,['bashcomplete_format','-o','%s '%(_tempfile)],outputlines,valattr)
        self.__resultok = True
        return


    def test_A012(self):
        commandline='''
        {
            "verbose|v" : "+",
            "jsonstr|j##jsonstr to read  none read from input or stdin##" : null,
            "basefile|B" : null,
            "jsonfile" : null,
            "optfile|F" : null,
            "extoptions|E" : null,
            "input|i" : null,
            "output|o" : null,
            "prefix|p" : null,
            "output<output_handler>" : {
                "$" : "*"
            },
            "release<release_handler>" : {
                "$" : "*"
            },
            "debug<debug_handler>" : {
                "$" : "*"
            },
            "verify<verify_handler>" : {
                "$" : 0
            },
            "version<version_handler>" : {
                "$" : 0
            },
            "selfcomp<selfcomp_handler>" : {
                "$" : 0
            }
        }        
        '''
        outputlines = []
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        self.__check_completion_output(commandline,['bashcomplete_format','-h','--'],outputlines,valattr)
        self.__check_bash_completion_output(commandline,['bashcomplete_format','-h','--'],outputlines,valattr)
        self.__resultok = True
        return

    def test_A013(self):
        options='''
        {
            "longprefix" : "-",
            "shortprefix" : "-",
            "nojsonoption" : true,
            "cmdprefixadded" : false
        }
        '''
        commandline='''
        {
            "asn1parse" : {
                "$" : 0,
                "$inform!optparse=inform_optparse;completefunc=inform_complete!" : null,
                "$in" : null,
                "$out" : null,
                "$noout" : false,
                "$offset" : 0,
                "$length" : -1,
                "$dump" : false,
                "$dlimit" : -1,
                "$oid" : null,
                "$strparse" : 0,
                "$genstr" : null,
                "$genconf" : null
            }
        }
        '''
        outputlines = []
        outputlines.extend(['-dlimit','-dump','-genconf','-genstr','-help','-in','-inform','-length'])
        outputlines.extend(['-noout','-offset','-oid','-out','-strparse'])
        outputlines.extend(['-h'])
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.additioncode='''
def inform_optparse(extparser,validx,keycls,params,firstcheck):
    extparser.warn_override(keycls,firstcheck)
    if validx >= (len(params) -1):
        # we do not check at the end of the file
        return 1
    valueform = params[validx]
    if valueform != 'DER' and valueform != 'PEM':
        message = '[%s'%(keycls.longopt)
        if keycls.shortflag is not None:
            message += '|%s'%(keycls.shortopt)
        message += '] must DER|PEM format'
        extparser.warn_message(message)
    if firstcheck:
        extparser.set_access(keycls)
    return 1

def inform_complete(extparser,validx,keycls,params,endwords=''):
    completions = []
    filtername = ''
    if len(params) > 0:
        filtername = params[-1]
    for c in ['PEM','DER']:
        retc = extparser.get_filter_name(c,filtername,endwords)
        if retc is not None:
            completions.append(retc)
    return completions
'''
        valattr.extoptions=options
        self.__check_completion_output(commandline,['openssl','asn1parse','-'],outputlines,valattr)
        self.__check_bash_completion_output(commandline,['openssl','asn1parse','-'],outputlines,valattr)
        return


    def test_A014(self):
        options='''
        {
            "longprefix" : "-",
            "shortprefix" : "-",
            "nojsonoption" : true,
            "cmdprefixadded" : false
        }
        '''
        commandline='''
        {
            "asn1parse" : {
                "$" : 0,
                "$inform!optparse=inform_optparse;completefunc=inform_complete!" : null,
                "$in" : null,
                "$out" : null,
                "$noout" : false,
                "$offset" : 0,
                "$length" : -1,
                "$dump" : false,
                "$dlimit" : -1,
                "$oid" : null,
                "$strparse" : 0,
                "$genstr" : null,
                "$genconf" : null
            }
        }
        '''
        outputlines = []
        outputlines.extend(['der','pem'])
        valattr = ValueAttr()
        if 'TEST_RELEASE' in os.environ.keys():
            valattr.releasemode = True
        valattr.additioncode='''
def inform_optparse(extparser,validx,keycls,params,firstcheck):
    extparser.warn_override(keycls,firstcheck)
    if validx >= (len(params) -1):
        # we do not check at the end of the file
        return 1
    valueform = params[validx]
    if valueform != 'der' and valueform != 'pem':
        message = '[%s'%(keycls.longopt)
        if keycls.shortflag is not None:
            message += '|%s'%(keycls.shortopt)
        message += '] must DER|PEM format'
        extparser.warn_message(message)
    if firstcheck:
        extparser.set_access(keycls)
    return 1

def inform_complete(extparser,validx,keycls,params,endwords=''):
    completions = []
    filtername = ''
    if len(params) > 0:
        filtername = params[-1]
    for c in ['pem','der']:
        retc = extparser.get_filter_name(c,filtername,endwords)
        if retc is not None:
            completions.append(retc)
    completions = sorted(completions)
    return completions
'''
        valattr.extoptions=options
        valattr.line = 'openssl asn1parse -inform '
        valattr.index = len(valattr.line)
        self.__check_completion_output(commandline,['openssl','asn1parse','-inform'],outputlines,valattr)
        self.__check_bash_completion_output(commandline,['openssl','asn1parse','-inform'],outputlines,valattr)
        return


    ##################################
    ## to check version
    ##
    ##################################
    def test_C001(self):
        if 'TEST_RELEASE' not in os.environ.keys():
            return
        versionstr = ''
        versionfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),'VERSION')
        format_release= os.path.join(os.path.dirname(os.path.realpath(__file__)),'bashcomplete_format')
        cmds = []
        cmds.append('%s'%(sys.executable))
        cmds.append(format_release)
        cmds.append('version')
        for l in cmdpack.run_cmd_output(cmds):
            versionstr = l.rstrip('\r\n')
        versionread = read_file(versionfile)
        versionread = versionread.rstrip('\r\n')
        self.assertEqual(versionread,versionstr)
        self.__resultok = True
        return

    def test_C002(self):
        if 'TEST_RELEASE' not in os.environ.keys():
            return
        supported = self.__expect_bash_supported()
        if not supported:
            return
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
        versionfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),'VERSION')
        versionstr = read_file(versionfile).rstrip('\r\n')
        jsonfile,runfile,templatefile,codef,optfile = self.__write_basic_files('output',commandline,'insertcode',None,None,None,True)
        child = self.__start_pexpect(runfile)
        # now we should give the echo
        child.send('echo "$INSERTCODE_COMPLETE_VERSION"\r\n')
        child.expect('INSERTCODE_COMPLETE_VERSION',timeout=0.3)
        child.expect('%s'%(versionstr),timeout=0.3)
        child.close()
        child.wait()
        child = None
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
        "releasemode" : false,
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
    if args.releasemode:
        os.environ['TEST_RELEASE'] = '1'
    else:
        if 'TEST_RELEASE' in os.environ.keys():
            del os.environ['TEST_RELEASE']
    newargs = []
    newargs.extend(args.args)
    sys.argv[1:]=newargs
    unittest.main(verbosity=args.verbose,failfast=args.failfast)
    return

if __name__ == '__main__':
    main()