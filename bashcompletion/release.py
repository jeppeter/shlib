#! /usr/bin/env python

import sys
import extargsparse
import os


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

def write_retfile(file,lines):
    s = ''
    if file is not None:
        with open(file,'ab') as f:
            for l in lines:
                f.write('%s\n'%(l))
    for l in lines:
        s += '%s\n'%(l)
    return s

def replace_output(s,pattern,infile=None,outfile=None):
    fin = sys.stdin
    fout = sys.stdout
    if infile is not None:
        fin= open(infile,'rb')
    if outfile is not None:
        fout = open(outfile,'wb')

    for l in fin:
        chgstr = l.replace(pattern,s)
        fout.write(chgstr)

    if fin != sys.stdin:
        fin.close()
    fin = None
    if fout != sys.stdout:
        fout.close()
    fout = None
    return

def release_file(args):
    repls = ''  
    for f in args.args:
        repls += read_file(f)
    replace_output(repls,args.pattern,args.input,args.output)
    return

def main():
    curdir=os.path.dirname(os.path.abspath(__file__))
    commandline_fmt='''
    {
        "verbose|v" : "+",
        "pattern|p" : "extended_opt_code=''",
        "input|i" : "%s",
        "output|o" : "%s",
        "$" : "*"
    }
    '''
    infile=os.path.join(curdir,'bashcomplete.py.tmpl')
    infile=infile.replace('\\','\\\\')
    outfile=os.path.join(curdir,'bashcomplete.py')
    outfile =outfile.replace('\\','\\\\')
    commandline=commandline_fmt%(infile,outfile)
    parser = extargsparse.ExtArgsParse(None,priority=[])
    parser.load_command_line_string(commandline)
    args = parser.parse_command_line()
    release_file(args)
    return

if __name__ == '__main__':
    main()

