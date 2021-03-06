#! /usr/bin/env python

import os
import extargsparse
import logging
import re
import sys
import tempfile

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

def __get_argsopt_opt(args,argsopt,subcmdname=None,needargs=True,shortopt=False):
    optret=[]
    opts = argsopt.get_cmdopts(subcmdname)
    if opts is not None:
        for c in opts:
            if c.type != 'args':
                if shortopt :
                    if needargs and c.nargs != 0 and c.shortflag is not None:
                        optret.append(c.shortflag)
                    elif not needargs and c.nargs == 0 and c.shortflag is not None:
                        optret.append(c.shortflag)
                else:
                    if  needargs and c.nargs != 0 :
                        optret.append(c.longopt)
                    elif not needargs and c.nargs == 0:
                        optret.append(c.longopt)
    return optret

def __get_argsopt_optattr(args,argsopt,opt,subcmdname=None):
    opts = argsopt.get_cmdopts(subcmdname)
    if opts is not None:
        if len(opt) == 1:            
            for c in opts:
                if c.type != 'args':
                    if c.shortflag is not None and c.shortflag == opt:
                        return c
        else:
            for c in opts:
                if c.type != 'args':
                    if c.longopt == opt:
                        return c
    return None

def get_argsopt_optattr(args,argsopt,opt,subcmdname=None):
    sarr = []
    if subcmdname is not None and len(subcmdname) > 0:
        sarr= re.split('\.',subcmdname)
    optattr = __get_argsopt_optattr(args,argsopt,opt,None)
    if optattr is not None:
        return optattr
    i = 0
    curcmd = ''
    while i < len(sarr):
        if i > 0:
            curcmd = '%s.%s'%(curcmd,sarr[i])
        else:
            curcmd = sarr[i]
        optattr = __get_argsopt_optattr(args,argsopt,opt,curcmd)
        if optattr is not None:
            return optattr
        i += 1
    return None

def get_argsopt_argsattr(args,argsopt,cmdname=None):
    opts = argsopt.get_cmdopts(cmdname)
    if opts is not None:
        for c in opts:
            if c.type =='args':
                return c
    return None

def __get_argsopt_longopt(args,argsopt,subcmdname=None,needargs=True):
    return __get_argsopt_opt(args,argsopt,subcmdname,needargs,False)

def __get_argsopt_noargs_longopt(args,argsopt,subcmdname=None):
    return __get_argsopt_longopt(args,argsopt,subcmdname,False)

def __get_argsopt_needargs_longopt(args,argsopt,subcmdname=None):
    return __get_argsopt_longopt(args,argsopt,subcmdname,True)

def __get_argsopt_shortopt(args,argsopt,subcmdname=None,needargs=True):
    return __get_argsopt_opt(args,argsopt,subcmdname,needargs,True)

def get_argsopt_opt(args,argsopt,cmdname=None,needargs=True,shortopt=False):
    sarr = []
    if cmdname is not None and len(cmdname) > 0:
        sarr = re.split('\.',cmdname)
    optret = []
    optret.extend(__get_argsopt_opt(args,argsopt,None,needargs,shortopt))
    if len(sarr) > 0:
        i = 0
        cmdname = ''
        while i < len(sarr):
            if i > 0:
                cmdname='%s.%s'%(cmdname,sarr[i])
            else:
                cmdname=sarr[i]
            optret.extend(__get_argsopt_opt(args,argsopt,cmdname,needargs,shortopt))
            i += 1
    return optret

def get_argsopt_longopt(args,argsopt,cmdname=None,needargs=True):
    return get_argsopt_opt(args,argsopt,cmdname,needargs,False)

def get_argsopt_needargs_longopt(args,argsopt,cmdname=None):
    return get_argsopt_longopt(args,argsopt,cmdname,True)

def get_argsopt_noargs_longopt(args,argsopt,cmdname=None):
    return get_argsopt_longopt(args,argsopt,cmdname,False)

def get_argsopt_shortopt(args,argsopt,cmdname=None,needargs=True):
    return get_argsopt_opt(args,argsopt,cmdname,needargs,True)

def get_argsopt_needargs_shortopt(args,argsopt,cmdname=None):
    return get_argsopt_shortopt(args,argsopt,cmdname,True)

def get_argsopt_noargs_shortopt(args,argsopt,cmdname=None):
    return get_argsopt_shortopt(args,argsopt,cmdname,False)

def get_argsopt_subcommand(args,argsopt,cmdname=None):
    return argsopt.get_subcommands(cmdname)

def write_retfile(file,lines):
    s = ''
    if file is not None:
        with open(file,'ab') as f:
            for l in lines:
                f.write('%s\n'%(l))
    for l in lines:
        s += '%s\n'%(l)
    return s

def get_command_name(args,argsopt,resfile,cmds):
    i=1
    maxwords = len(cmds) - 1
    retcmd=''
    errors = ''
    while i < maxwords:
        curcmd = cmds[i]
        i += 1
        if curcmd == '--':
            retcmd='+%d-%s'%((i-1),retcmd)
            break
        if curcmd.startswith('--'):
            if curcmd in get_argsopt_needargs_longopt(args,argsopt,retcmd):
                i += 1
            elif curcmd in get_argsopt_noargs_longopt(args,argsopt,retcmd):
                pass
            else:
                logging.info('[%d][%s] not valid opts'%(i,curcmd))
                retcmd='--'
                errors += write_retfile(resfile,['[%d] not valid [%s]'%((i-1),curcmd),'please check opt'])
                break
        elif curcmd.startswith('-'):
            j = 1
            shortstep = 0
            while j < len(curcmd):
                curch = curcmd[j]
                if curch in get_argsopt_needargs_shortopt(args,argsopt,retcmd):
                    if shortstep > 0:
                        logging.info('[%d][%d][%s] multiple need args for opt'%(i,j,curch))
                        retcmd='--'
                        errors += write_retfile(resfile,['[%d][%s] multiple need args defined'%(i,curcmd),'please check for options use -h|--help'])
                        break
                    shortstep += 1
                elif curch in get_argsopt_noargs_shortopt(args,argsopt,retcmd):
                    pass
                else:
                    retcmd='--'
                    logging.info('[%d][%d][%s] not defined shortopt'%(i,j,curch))
                    errors += write_retfile(resfile,['[%d][%s] not defined shortopt'%(i,curcmd),'please check for options use -h|--help'])
                    break
                j += 1
            if shortstep > 0:
               i += 1
        else:
            if curcmd in get_argsopt_subcommand(args,argsopt,retcmd):
                if len(retcmd) > 0:
                    retcmd = '%s.%s'%(retcmd,curcmd)
                else:
                    retcmd = curcmd
            else:
                retcmd = '+%d-%s'%((i-1),retcmd)
                break
    return retcmd,errors
                

def remove_file(args,infile):
    logging.info('remove [%s]'%(infile))
    if infile is not None and not args.reserved and os.path.exists(infile):
        os.remove(infile)
    return

def make_tempfile(dirn=None,suffix=''):
    temf,fd= tempfile.mkstemp(suffix,dir=dirn)
    os.close(fd)
    return tempf

def __get_argsopt_optfunc_opt(args,argsopt,opt,cmdname=None,shortflag=False):
    optfunc = None
    opts = argsopt.get_cmdopts(cmdname)
    if opts is not None:
        for c in opts:
            if c.type != 'args':                
                if not shortflag and c.longopt == opt:
                    if c.attr is not None:
                        if c.attr.optfunc is not None:
                            optfunc = c.attr.optfunc
                    break
                elif shortflag and c.shortflag is not None and c.shortflag == opt:
                    if c.attr is not None:
                        if c.attr.optfunc is not None:
                            optfunc = c.attr.optfunc
                    break
    return optfunc

def get_argsopt_optfunc_opt(args,argsopt,opt,cmdname=None,shortflag=False):
    sarr = []
    optfunc = None
    if cmdname is not None and len(cmdname) > 0:
        sarr = re.split('\.',cmdname)

    optfunc = __get_argsopt_optfunc_opt(args,argsopt,opt,None,shortflag)
    if optfunc is not None:
        return optfunc
    i = 0
    curcmd = ''
    while i < len(sarr):
        if i > 0:
            curcmd = '%s.%s'%(curcmd,sarr[i])
        else:
            curcmd='%s'%(sarr[i])
        optfunc = __get_argsopt_optfunc_opt(args,argsopt,opt,curcmd,shortflag)
        if optfunc is not None:
            return optfunc
        i += 1
    return None

def get_argsopt_optfunc_shortopt(args,argsopt,shortopt,cmdname=None):
    return get_argsopt_optfunc_opt(args,argsopt,shortopt,cmdname,True)

def get_argsopt_optfunc_longopt(args,argsopt,longopt,cmdname=None):
    return get_argsopt_optfunc_opt(args,argsopt,longopt,cmdname,False)

def get_argsopt_cmdfunc(args,argsopt,cmdname=None):
    cmdfunc = None
    opts = argsopt.get_cmdopts(cmdname)
    if opts is not None:
        for c in opts:
            if c.type == 'args':
                if c.attr is not None and c.attr.optfunc is not None:
                    cmdfunc=c.attr.optfunc
                    break
    return cmdfunc

def call_optfunc(funcname,args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs):
    s = ''
    m = importlib.import_module('__main__')
    if m is not None:
        funcptr = getattr(m,funcname,None)
        if funcptr is not None or not hasattr(funcptr,'__call__'):
            raise Exception('%s not defined '%(funcname))
        s = funcptr(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)
    return s

def file_filter(p):
    return os.path.isfile(p)

def dir_filter(p):
    return os.path.isdir(p)

def file_common_completion(basedir,pathpat,filterop=None):
    retfiles = []
    for c in os.listdir(basedir):
        ok = True
        ofile = os.path.join(basedir,c)
        if filterop is not None:
            ok = filterop(ofile)
        if ok and (len(pathpat) == 0 or ofile.startswith(pathpat)):
            retfiles.append(ofile)
    return retfiles


def all_file_completion(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs):
    pathpat= ''
    if len(totalargs) > 1:
        pathpat = totalargs[-1]
    if pathpat.startswith('/'):
        basedir = os.path.dirname(pathpat)
    else:
        basedir = os.path.dirname(pathpat)
    if len(basedir) == 0:
        basedir = '.'
    retfiles = file_common_completion(basedir,pathpat,None)
    logging.info('retfiles (%s)'%(retfiles))
    return write_retfile(resfile,retfiles)

def basic_common_completion_opt(longopt,args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs):
    s = ''
    optattr = get_argsopt_optattr(args,argsopt,longopt,cmdname)
    if optattr is None:
        raise Exception('inner error in [%s] longopt'%(longopt))
    if optattr.type == 'int' or optattr.type == 'long':
        s += write_retfile(resfile,['int %s...'%(totalargs[-1]),'[%s] handle'%(longopt)])
        return s
    elif optattr.type == 'float':
        s += write_retfile(resfile,['float %s...'%(totalargs[-1]),'[%s] handle'%(longopt)])
        return s
    elif optattr.type == 'jsonfile' or optattr.type == 'string' \
        or optattr.type == 'list' or optattr.type == 'unicode':
        s += all_file_completion(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)
        return s
    return s

def basic_common_completion_withoutopt(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs):
    argsattr = get_argsopt_argsattr(args,argsopt,cmdname)
    if argsattr is not None:
        if argsattr.nargs == '0':
            # we do not output any output
            return ''
    return all_file_completion(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)

def basic_common_completion_option(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs):
    lastarg = ''
    outputargs = []
    if len(totalargs) > 1:
        lastarg = totalargs[-1]
    logging.info('start need args longopt')
    for c in get_argsopt_needargs_longopt(args,argsopt,cmdname):
        if  len(lastarg) == 0 or c.startswith(lastarg):
            logging.info('add [%s]'%(c))
            outputargs.append(c)
    logging.info('start no args longopt')
    for c in get_argsopt_noargs_longopt(args,argsopt,cmdname):
        if len(lastarg) == 0 or c.startswith(lastarg):
            logging.info('add [%s]'%(c))
            outputargs.append(c)
    if len(lastarg) == 0 or (lastarg.startswith('-') and not lastarg.startswith('--')):
        shortstep = 0
        j = 1
        while j < len(lastarg):
            curch = lastarg[j]
            if curch in get_argsopt_needargs_shortopt(args,argsopt,cmdname):
                shortstep += 1
            j += 1
        if shortstep > 1:
            # this is not the valid one ,so we should make this not ok
            return write_retfile(resfile,['[%s] add need args short opt more than one'%(lastarg),'please use -h|--help to see']),False
        if shortstep == 0:
            logging.info('start need args shortopt')
            for c in get_argsopt_needargs_shortopt(args,argsopt,cmdname):
                if lastarg.startswith('-'):
                    logging.info('add [%s]'%(c))
                    outputargs.append('%s'%(c))
                else:
                    logging.info('add [-%s]'%(c))
                    outputargs.append('-%s'%(c))
        logging.info('start no args shortopt')
        for c in get_argsopt_noargs_shortopt(args,argsopt,cmdname):
            if lastarg.startswith('-'):
                logging.info('add [%s]'%(c))
                outputargs.append('%s'%(c))
            else:
                logging.info('add [-%s]'%(c))
                outputargs.append('-%s'%(c))
    return write_retfile(resfile,outputargs),True

def basic_common_completion(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs):
    s = ''
    curs , ok = basic_common_completion_option(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)
    s += curs
    if not ok:
        return s
    s += basic_common_completion_withoutopt(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)
    return s

def format_completion(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs):
    prevopt = None
    if len(totalargs) > 2:
        prevopt = totalargs[-2]
    logging.info('cmdidx [%d] len(%d)'%(cmdidx,len(totalargs)))
    if cmdidx == (len(totalargs) - 1):
        if prevopt is not None:
            if prevopt.startswith('--'):
                for prevopt in get_argsopt_needargs_longopt(args,argsopt,cmdname):
                    optfunc = get_argsopt_optfunc_longopt(args,argsopt,prevopt,cmdname)
                    if optfunc is not None:
                        return call_optfunc(optfunc,args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)
                    return basic_common_completion_opt(prevopt,args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)
            elif prevopt.startswith('-'):
                totallen = len(prevopt)
                j = 1
                while j < totallen:
                    curch = prevopt[j] 
                    if curch in get_argsopt_needargs_shortopt(args,argsopt,cmdname):
                        optfunc = get_argsopt_optfunc_shortopt(args,argsopt,curch,cmdname)
                        if optfunc is not None:
                            return call_optfunc(optfunc,args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)
                        return basic_common_completion_opt(curch,args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)
                    j += 1
        # now we should 
        return basic_common_completion(args,argsopt,resfile,cmdidx,cmdname,leftargs,totalargs)
    else:
        # this is the 
        subcmds = argsopt.get_subcommands(cmdname)
        if subcmds is not None and len(subcmds) != 0:
            return write_retfile(resfile,['cmdname [%s]'%(cmdname),'please use -h|--help to see help'])
        argsattr = get_argsopt_argsattr(args,argsopt,cmdname)
        if argsattr.nargs == '*' or argsattr.nargs == '+':
            pass
        elif argsattr.nargs == '?':
            return write_retfile(resfile,['cmdname [%s] just need one args'%(cmdname),'please use -h|--help to see help'])
        else:
            argscnt = int(argsattr.nargs)
            if argscnt > (len(totalargs) - cmdidx - 1):
                return write_retfile(resfile,['cmdname [%s] more than %d'%(cmdname,argscnt),'please use -h|--help to see help'])
        return basic_common_completion_withoutopt(args,argsopt,cmdidx,cmdname,leftargs,totalargs)





def completion_format(args):
    s = ''
    if args.jsonstr is None:
        args.jsonstr = read_file()
    argsopt = extargsparse.ExtArgsParse(None,priority=[])
    argsopt.load_command_line_string(args.jsonstr)
    #tempf = make_tempfile()
    tempf = None
    cmdname ,errors = get_command_name(args,argsopt,tempf,args.args)
    if cmdname == '--':
        s += errors
        remove_file(args,tempf)
        return s
    if cmdname.startswith('+'):
        idxexpr = re.compile('^\+([\d]+)-([\w\.]*)')
        mg = idxexpr.findall(cmdname)
        if len(mg) < 0 or len(mg[0]) < 2:
            raise Exception('(%s) not valid startswith +'%(cmdname))
        cmdidx = int(mg[0][0])
        cmdname = mg[0][1]
        leftargs = args.args[cmdidx:]
    else:
        cmdidx = len(args.args) - 1
        leftargs = args.args[cmdidx:]
    s += format_completion(args,argsopt,tempf,cmdidx,cmdname,leftargs,args.args)
    remove_file(args,tempf)
    return s
    

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
        "reserved|R##to reserve temp file##" : false,
        "jsonparse|j##if not set ,input json string from stdin##" : null,
        "output|o" : null,
        "$" : "*"
    }
    '''
    parser = extargsparse.ExtArgsParse(options=None,priority=[])
    parser.load_command_line_string(commandline)
    args = parser.parse_command_line()
    set_log_level(args)
    try:        
        s = completion_format(args)
    except:
        trback = sys.exc_info()[2]
        exceptname = sys.exc_info()[1]
        s = ''
        s += 'exception %s:\n'%(exceptname)
        s +='trace back:\n'
        s += get_full_trace_back(trback,1,0)
        sys.stderr.write('%s'%(s))
        return
    output_string(s,args.output)
    return

if __name__ == '__main__':
    main()