
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
        self.warn_message(message)
    if firstcheck:
        self.set_access(keycls)
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