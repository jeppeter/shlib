#! /usr/bin/python

import extargsparse
import sys
import extargsparse
import logging
import os
import random
import bz2
import base64
import time


##debugoutstart


##debugoutend

def _add_path(curpath,*paths):
    testfile = os.path.join(curpath,*paths)
    if os.path.exists(testfile):
        if curpath != sys.path[0]:
            if curpath in sys.path:
                sys.path.remove(curpath)
            oldpath=sys.path
            sys.path = [curpath]
            sys.path.extend(oldpath)
    return


def make_dir_safe(dname=None):
    if dname is not None:
        if not os.path.isdir(dname):
            try:
                os.makedirs(dname)
            except:
                pass
            if not os.path.isdir(dname):
                raise Exception('can not make [%s]'%(dname))


def make_tempfile(prefix=None,suffix=''):
    make_dir_safe(prefix)
    fd,result = tempfile.mkstemp(suffix=suffix,dir=prefix)
    os.close(fd)
    f = os.path.abspath(os.path.realpath(result))
    return f


def read_file(infile=None):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')
    for l in fin:
        if sys.version[0] == '2':
            s += l
        else:
            s += l.decode(encoding='UTF-8')
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def write_file(s,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile,'wb')
    if sys.version[0] == '2':
        fout.write('%s'%(s))
    else:
        bs = s.encode(encoding='UTF-8')
        if fout == sys.stdout:
            fout.write(s)
        else:
            fout.write(bs)
    if fout != sys.stdout:
        fout.close()
    fout = None
    return 

def replace_outputs(s,pattern,instrs=None):
    rets = ''
    rets += instrs.replace(pattern,s)
    return rets

def __get_sh_python(args,ins):
    s = ''
    for l in ins:
        for c in l:
            if c == '\n':
                s += '\\'
                s += 'n'
            elif c == '$':
                s += '\\'
                s += '$'
            elif c == '"':
                s += '\\'
                s += '"'
            elif c == '\\':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '\\'
            elif c == '`':
                s += '\\'
                s += '`'
            elif c == '\r':
                s += '\\'
                s += 'r'
            elif c == '\t':
                s += '\\'
                s += 't'
            elif c == '\'':
                s += '\\\\'
                s += '\''
            else:
                s += c
    return s

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

def __format_tab_line(s,tabs=0):
    outs = ' ' * tabs * 4
    outs += '%s\n'%(s)
    return outs

def get_bash_complete_string(args,newargspattern):
    hprefix = args.prefix.upper()
    lprefix = args.prefix.lower()
    s = ''
    s += __format_tab_line('#! /bin/bash')
    s += __format_tab_line('read -r -d \'\' %s_COMMAND_JSON_OPTIONS<<%s_EOFMM'%(hprefix,newargspattern))
    s += __format_tab_line(args.jsonstr)
    s += __format_tab_line('%s_EOFMM'%(newargspattern))
    s += __format_tab_line('')
    s += __format_tab_line('%s_PYTHON_COMPLETE_STR="c=\'%%%s%%\';exec(c);"'%(hprefix,newargspattern))
    s += __format_tab_line('')
    s += __format_tab_line('_%s_complete()'%(lprefix))
    s += __format_tab_line('{')
    s += __format_tab_line('local _verbosemode=""',1)
    s += __format_tab_line('if [ -n "$%s_DEBUG_MODE" ] && [ $%s_DEBUG_MODE -gt 0 ]'%(hprefix,hprefix),1)
    s += __format_tab_line('then',2)
    s += __format_tab_line('_verbosemode="-vvvv"',2)
    s += __format_tab_line('fi',1)
    s += __format_tab_line('if [ -z "$PYTHON"]',1)
    s += __format_tab_line('then',2)
    s += __format_tab_line('PYTHON=python',2)
    s += __format_tab_line('fi',1)
    s += __format_tab_line('',1)
    s += __format_tab_line('COMPREPLY=($(echo -n "$%s_COMMAND_JSON_OPTIONS" | $PYTHON -c "$%s_PYTHON_COMPLETE_STR" $_verbosemode --line "${COMP_LINE}" --index "${COMP_POINT}" --  "${COMP_WORDS[@]}"))'%(hprefix,hprefix),1)
    s += __format_tab_line('}')
    s += __format_tab_line('complete -F _%s_complete %s'%(lprefix,args.prefix))
    return s

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

def unzip_format_string(instr):
    if type(instr) == 'bytes' and sys.version[0] == '3':
        instr = instr.decode(encoding='UTF-8')
    instr = instr.replace('\r','')
    instr = instr.replace('\n','')
    encstr = base64.b64decode(instr)
    return bz2.decompress(encstr)

def base_get_base_string(args):
    if args.basefile is None:
        raise Exception('please specified basefile by [--basefile|-B]')
    return read_file(args.basefile)

def format_get_base_string():
    return unzip_format_string(BASH_COMPLETE_STRING)

def get_base_string(args):
    return base_get_base_string(args)

def __get_priority(inputprior):
    priority = None
    if len(inputprior) == 0 or (len(inputprior) == 1 and inputprior[0] == 'NONE'):
        pass
    else:
        priority = []
        for c in inputprior:
            if c == 'SUBCMD_JSON' :
                priority.append(extargsparse.SUB_COMMAND_JSON_SET)
            elif c == 'CMD_JSON' :
                priority.append(extargsparse.COMMAND_JSON_SET)
            elif c == 'ENV_SUBCMD_JSON' :
                priority.append(extargsparse.ENV_SUB_COMMAND_JSON_SET)
            elif c == 'ENV_CMD_JSON':
                priority.append(extargsparse.ENV_COMMAND_JSON_SET)
            elif c == 'ENV_CMD' :
                priority.append(extargsparse.ENVIRONMENT_SET)
            elif c == 'NONE':
                break
            else:
                raise Exception('unknown priority (%s)'%(c))
    return priority


def __check_function(parser,mod,cmdname=''):
    subcmds = parser.get_subcommands(cmdname)
    if subcmds is not None:
        for c in subcmds:
            curcmd = cmdname
            if len(curcmd) > 0:
                curcmd += '.'
            curcmd += c
            __check_function(parser,mod,curcmd)
    cmdopts = parser.get_cmdopts(cmdname)
    if cmdopts is not None:
        for opt in cmdopts:
            if not opt.isflag:
                continue
            if opt.attr is not None and opt.attr.optparse is not None:
                funcptr = getattr(mod,opt.attr.optparse,None)
                if funcptr is None:
                    raise Exception('can not find optparse [%s]'%(opt.attr.optparse))
            if opt.attr is not None and opt.attr.completefunc is not None:
                funcptr = getattr(mod,opt.attr.completefunc,None)
                if funcptr is None:
                    raise Exception('can not find optparse [%s]'%(opt.attr.completefunc))
    return



def check_functions(jsonstr,pythonstr,extoptstr=None):
    tempf = None
    try:
        tempf = make_tempfile(prefix=None,suffix='.py')
        with open(tempf,'w') as fout:
            fout.write('%s'%(pythonstr))
        options = extargsparse.ExtArgsOptions(extoptstr)
        priority = None
        if options.priority is not None:
            priority = __get_priority(options.priority)
        parser = extargsparse.ExtArgsOptions(options,priority)
        tempd = os.path.dirname(os.path.realpath(tempf))
        _add_path(tempd)
        pymod = os.path.basename(os.path.realpath(tempf))
        pymod = pymod.replace('\.py$','')
        mod = importlib.import_module(pymode)
        __check_function(parser,mod)
    finally:
        if tempf is not None:
            os.remove(tempf)
        tempf = None
    return


def output_handler(args,parser):
    set_log_level(args)
    if args.prefix is None:
        raise Exception('please specified release')
    if args.jsonstr is None:
        args.jsonstr = read_file(args.input)
    args.pattern = "extended_opt_code=''"
    extrastr = ''
    for c in args.subnargs:
        extrastr += read_file(c)
    base_string = read_file(args.basefile)
    logging.info('base_string (%d)'%(len(base_string)))
    python_string = replace_outputs(extrastr,args.pattern,base_string)
    check_functions(args.jsonstr,python_string,args.extoptions)
    # now w
    newargspattern = 'REPLACE_PATTERN'
    while True:
        newstr = args.jsonstr.replace('%%%s%%'%(newargspattern),'')
        # it means that the coding 
        if newstr != args.jsonstr:
            newargspattern = get_temp_value()
            continue
        newstr = args.jsonstr.replace('%s'%(newargspattern),'')
        if newstr != args.jsonstr:
            newargspattern = get_temp_value()
            continue
        newstr = python_string.replace('%%%s%%'%(newargspattern),'')
        # it means that the 
        if newstr != python_string:
            newargspattern = get_temp_value()
            continue
        newstr = python_string.replace('%s'%(newargspattern),'')
        if newstr != python_string:
            newargspattern = get_temp_value()
            continue

        if args.extoptions is not None:
            newstr = args.extoptions.replace('%%%s%%'%(newargspattern),'')
            if newstr != args.extoptions:
                newargspattern = get_temp_value()
                continue
            newstr = args.extoptions.replace('%s'%(newargspattern),'')
            if newstr != args.extoptions:
                newargspattern = get_temp_value()
                continue
        break        
    bash_base_string=get_bash_complete_string(args,newargspattern)
    shpython_string = __get_sh_python(args,python_string)
    bash_complete_string = replace_outputs(shpython_string,'%%%s%%'%(newargspattern),bash_base_string)
    bash_complete_string = bash_complete_string.replace('\r','')
    write_file(bash_complete_string,args.output)
    # now to try out

    sys.exit(0)
    return

def bzip2_base64_encode(instr):
    logging.debug('instr type(%s)'%(type(instr)))
    if sys.version[0] == '2':
        instr = instr
    else:
        instr = instr.encode(encoding='UTF-8')
    encstr = bz2.compress(instr)
    b64str = base64.b64encode(encstr)
    logging.info('b64str type(%s)'%(type(b64str)))
    if sys.version[0] == '3':
        b64str = b64str.decode(encoding='UTF-8')
    outs = ''
    c = 0
    while c < len(b64str):
        if c > 0:
            outs += '\n'
        cnt = 80
        if len(b64str) < (c + cnt):
            cnt = len(b64str) - c
        outs +=  b64str[c:(c+cnt)]
        c += cnt
    return outs

def outstr_repls(repls,pattern,infile=None,outfile=None):
    fout = sys.stdout
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    if outfile is not None:
        fout = open(outfile,'wb')

    for l in fin:
        if sys.version[0] == '2':
            bl = l.replace(pattern,repls)
        else:
            bl = l.decode(encoding='UTF-8')
            bl = bl.replace(pattern,repls)
            bl = bl.encode(encoding='UTF-8')
        fout.write(bl)

    if fin != sys.stdin:
        fin.close()
    fin = None

    if fout != sys.stdout:
        fout.close()
    fout = None
    return

def release_handler(args,parser):
    set_log_level(args)
    if args.basefile is None:
        raise Exception('please specified basefile by [--basefile|-B]')
    if args.pattern is None:
        args.pattern = '%BASH_COMPLETE_STRING%'
    basestr = read_file(args.basefile)
    logging.info('basestring (%s)'%(basestr))
    basestr = bzip2_base64_encode(basestr)
    logging.info('basestring (%s)'%(basestr))
    outstr_repls(basestr,args.pattern,args.input,args.output)
    sys.exit(0)
    return

def debug_handler(args,parser):
    set_log_level(args)
    if args.basefile is None:
        raise Exception('can not handle basefile ok')
    args.pattern = "extended_opt_code=''"
    extrastr = ''
    for c in args.subnargs:
        extrastr += read_file(c)
    base_string = read_file(args.basefile)
    logging.info('base_string (%d)'%(len(base_string)))
    python_string = replace_outputs(extrastr,args.pattern,base_string)
    write_file(python_string,args.output)
    sys.exit(0)
    return

def main():
    commandline='''
    {
        "verbose|v" : "+",
        "jsonstr|j##jsonstr to read  none read from input or stdin##" : null,
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
        }
    }
    '''
    random.seed(time.time())
    parser = extargsparse.ExtArgsParse(None,priority=[])
    parser.load_command_line_string(commandline)
    parser.parse_command_line(None,parser)
    raise Exception('can not run here without specified subcommand')
    return


BASH_COMPLETE_STRING='''
%BASH_COMPLETE_STRING%
'''

if __name__ == '__main__':
    main()
