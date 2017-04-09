#! /usr/bin/env python

import pexpect
import os
import sys
import re
import logging
import time

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


class RunObject(object):
    def __init__(self):
        self.__verbose = 3
        self.__tempfiles = []
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


    def run_code(self,runfile,timeout=0.3):
        child = self.__start_pexpect(runfile)
        child.send('openssl ca -')
        child.expect('openssl ca -',timeout=timeout)
        child.send('\t')
        readbuf = get_read_completion(child,timeout=timeout)
        child.send('\t')
        readbuf = get_read_completion(child,timeout=timeout)
        child.send('\t')
        readbuf = get_read_completion(child,timeout=timeout)
        idx = 0
        idx += 1
        print('[%d][%s]'%(idx,readbuf))
        child.close()
        child.wait()
        child = None
        return readbuf


def main():
    robj = RunObject()
    buf = robj.run_code(sys.argv[1])
    print('buf [%s]'%(buf))
    return

main()
