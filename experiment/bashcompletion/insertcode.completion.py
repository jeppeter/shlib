#! /usr/bin/env python

import os
import extargsparse
import logging
import re
import sys

def read_file(infile=None):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')
    for l in fin:
        s += l
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_command_line(args,argsopt):

def completion_fomat(args):
    s = ''
    if args.jsonstr is None:
        args.jsonstr = read_file()
    argsopt = extargsparse.ExtArgsParse(None,priority=[])
    argsopt.load_command_line_string(args.jsonstr)

    

def output_string(s,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile,'wb')
    fout.write('%s'%(s))
    if fout != sys.stdout:
        fout.close()
    fout = None
    return

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


def main():
    commandline='''
    {
        "verbose|v" : "+",
        "jsonparse|j##if not set ,input json string from stdin##" : null,
        "output|o" : null,
        "$" : "*"
    }
    '''
    parser = extargsparse.ExtArgsParse(options=None,priority=[])
    parser.load_command_line_string(commandline)
    args = parser.parse_command_line()
    try:
        s = completion_format(args)
    except:
        trback = sys.exc_info()[2]
        s ='trace back:\n'
        s += get_full_trace_back(trback,1,0)
        sys.stderr.write('%s'%(s))
        return
    output_string(s,args.output)
    return

if __name__ == '__main__':
    main()