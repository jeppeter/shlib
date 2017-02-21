
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
CURDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' .)


ifeq (${V},)
Q=@
else
Q=
endif

include ${TOPDIR}/basedef.mak

all:mkcode

mkcode:mkcode.tmpl check_libs ${TOPDIR}/pysrc/calcmd5.py ${TOPDIR}/perlsrc/basename.pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i mkcode.tmpl  -p '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} ${TOPDIR}/insertcode -p '%DEFINESH_CODE%' bashinsert "${TOPDIR}/libs/definesh" | \
		${PYTHON} ${TOPDIR}/insertcode -p '%PERL_BASE_NAME%' bashstring "${TOPDIR}/perlsrc/basename.pl" | \
		${PYTHON} ${TOPDIR}/insertcode -p '%PYTHON_MD5_STR%' bashstring ${TOPDIR}/pysrc/calcmd5.py | \
		${PYTHON} ${TOPDIR}/insertcode -o mkcode -p '%DEPENDSH_CODE%' bashinsert "${TOPDIR}/libs/dependsh","GENSH",$@)
	$(call call_exec,${CHX} mkcode,"CHX","mkcode")

check_libs:check_calcmd5_py check_basename_pl

check_calcmd5_py:${TOPDIR}/pysrc/calcmd5.py

check_basename_pl:${TOPDIR}/perlsrc/basename.pl

check_%_py:${TOPDIR}/pysrc/%.py
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl bashstring $< | ${BASH} | ${DIFF} - $<,"CHECK","$(<F)")


check_%_pl:${TOPDIR}/perlsrc/%.pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl bashstring $< | ${BASH} | ${DIFF} - $<,"CHECK","$(<F)")

clean:
	$(call call_exec,rm -f mkcode *.tmp,"RM","mkcode *.tmp")
