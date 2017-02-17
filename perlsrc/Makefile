
ifeq (${V},)
Q=@
else
Q=
endif

include ../basedef.mak

TOPDIR:=$(shell perl -e 'use Cwd "abs_path";print abs_path(shift);' -- ..)
CURDIR:=$(shell perl -e 'use Cwd "abs_path";print abs_path(shift);' -- .)


ORIG_PERLS = dos2unix.pl iscsiinfo.pl replacedir.pl 

TEMPLATE_PERLS = basename.pl defval.pl dephandle.pl exename.pl filterop.pl getdep.pl maketarget.pl mountcheck.pl 
TEMPLATE_PERLS += readlink.pl shortname.pl subpath.pl toobj.pl

PERL_FILES =  ${ORIG_PERLS} ${TEMPLATE_PERLS}

all: ${PERL_FILES}

%.pl : %.pl.tmpl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i $< -p '%COMMON_PL_CODE%' -o $@ bashinsert ${CURDIR}/common.pl,"GENPL","$(@F)")
	$(call call_exec,${PERL} $@ -h >/dev/null,"CHECK","$(@F)")

clean:
	$(call call_exec,${RM} -f ${TEMPLATE_PERLS},"RM","TEMPLATE_PERLS")