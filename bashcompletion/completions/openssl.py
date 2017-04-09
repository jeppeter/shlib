
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

def cmsform_optparse(extparser,validx,keycls,params,firstcheck):
    extparser.warn_override(keycls,firstcheck)
    if validx >= (len(params) -1):
        # we do not check at the end of the file
        return 1
    valueform = params[validx]
    if valueform != 'DER' and valueform != 'PEM' and valueform != 'SMIME':
        message = '[%s'%(keycls.longopt)
        if keycls.shortflag is not None:
            message += '|%s'%(keycls.shortopt)
        message += '] must DER|PEM|SMIME format'
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
    completions = sorted(completions)
    return completions

def cmsform_complete(extparser,validx,keycls,params,endwords=''):
    completions = []
    filtername = ''
    if len(params) > 0:
        filtername = params[-1]
    for c in ['PEM','DER','SMIME']:
        retc = extparser.get_filter_name(c,filtername,endwords)
        if retc is not None:
            completions.append(retc)
    completions = sorted(completions)
    return completions