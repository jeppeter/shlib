
TOPDIR:=$(shell perl -e 'use Cwd "abs_path";print abs_path(shift);' ..)
CURDIR:=$(shell perl -e 'use Cwd "abs_path";print abs_path(shift);' .)

ifeq (${V},)
Q=@
else
Q=
endif

ifeq (${M},)
MINNUM=10
else
MINNUM=${M}
endif

ifeq (${X},)
MAXNUM=20
else
MAXNUM=${X}
endif

TEMPLATE_MAKS = basedef.mak  fileop.mak varop.mak depop.mak makelib.mak

include ${TOPDIR}/basedef.mak



remake:
	$(call call_exec,${MAKE} --no-print-directory -C ${CURDIR} -f $(firstword ${MAKEFILE_LIST}) clean,"REMAKE","CLEAN")
	$(call call_exec,${MAKE} --no-print-directory -C ${CURDIR} -f $(firstword ${MAKEFILE_LIST}) all,"REMAKE","ALL")


all:test

test:testmak.py

testmak.py:makelib.mak Makefile
	$(call call_exec,${PYTHON} ${CURDIR}/testmak.py -f --minnum ${MINNUM} --maxnum ${MAXNUM} >/dev/null,"TEST","makelib")

makelib.mak: makelib.mak.tmpl basedef.mak varop.mak exec.mak fileop.mak depop.mak 
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i $< -p '%BASEDEF_MAK%' bashinsert ${CURDIR}/basedef.mak |\
		  ${PYTHON} ${TOPDIR}/insertcode -p '%VAROP_MAK%' bashinsert ${CURDIR}/varop.mak | \
		  ${PYTHON} ${TOPDIR}/insertcode -p '%EXEC_MAK%' bashinsert ${CURDIR}/exec.mak | \
		  ${PYTHON} ${TOPDIR}/insertcode -p '%FILEOP_MAK%' bashinsert ${CURDIR}/fileop.mak | \
		  ${PYTHON} ${TOPDIR}/insertcode -p '%DEPOP_MAK%' -o $@ bashinsert ${CURDIR}/depop.mak,"MAK","$(@F)")

basedef.mak:basedef.mak.tmpl ${CURDIR}/VERSION
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i $< -p '%MAKELIB_VERSION%' -o $@ bashinsert ${CURDIR}/VERSION,"MAK","$(@F)") 

fileop.mak:fileop.mak.tmpl ${TOPDIR}/perlsrc/readlink.pl ${TOPDIR}/perlsrc/exename.pl  \
	${TOPDIR}/perlsrc/toobj.pl ${TOPDIR}/perlsrc/filterop.pl ${TOPDIR}/perlsrc/basename.pl ${TOPDIR}/perlsrc/getdep.pl \
	${TOPDIR}/perlsrc/getsoname.pl
	$(call call_exec,${MAKE} --no-print-directory -C . check_readlink_pl check_shortname_pl check_exename_pl check_toobj_pl  check_filterop_pl check_basename_pl check_getdep_pl check_getsoname_pl,"CHECKPL","fileop.mak")
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode  -i $< -p '%PERL_READLINK_STR%' makestring ${TOPDIR}/perlsrc/readlink.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_EXENAME_STR%' makestring ${TOPDIR}/perlsrc/exename.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_TOOBJ_STR%' makestring ${TOPDIR}/perlsrc/toobj.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_FILTEROP_STR%' makestring ${TOPDIR}/perlsrc/filterop.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_GETDEP_STR%' makestring ${TOPDIR}/perlsrc/getdep.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_GETSONAME_STR%' makestring ${TOPDIR}/perlsrc/getsoname.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_BASENAME_STR%' -o $@ makestring ${TOPDIR}/perlsrc/basename.pl,"MAK","$(@F)")

check_readlink_pl:${TOPDIR}/perlsrc/readlink.pl

check_getdep_pl:${TOPDIR}/perlsrc/getdep.pl


varop.mak:varop.mak.tmpl ${TOPDIR}/perlsrc/shortname.pl ${TOPDIR}/perlsrc/defval.pl
	$(call call_exec,${MAKE} --no-print-directory -C . check_shortname_pl check_defval_pl,"CHECKPL","varop.mak")
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i $< -p '%PERL_SHORTNAME_STR%'  makestring ${TOPDIR}/perlsrc/shortname.pl | \
		${PYTHON} ${TOPDIR}/insertcode -p '%PERL_DEFVAL_STR%' -o $@ makestring ${TOPDIR}/perlsrc/defval.pl,"MAK","$(@F)")


check_shortname_pl:${TOPDIR}/perlsrc/shortname.pl

check_defval_pl:${TOPDIR}/perlsrc/defval.pl

check_exename_pl:${TOPDIR}/perlsrc/exename.pl

check_toobj_pl:${TOPDIR}/perlsrc/toobj.pl

check_filterop_pl:${TOPDIR}/perlsrc/filterop.pl

check_dephandle_pl:${TOPDIR}/perlsrc/dephandle.pl

check_basename_pl:${TOPDIR}/perlsrc/basename.pl

check_getsoname_pl:${TOPDIR}/perlsrc/getsoname.pl

check_%_pl:${TOPDIR}/perlsrc/%.pl
	$(call call_exec,(${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' \
		bashstring $< | ${BASH} | ${DIFF} -B - $< ) || \
		(${ECHO} "can not make $< right" >&2 ; exit 3),\
		"CHECK","$(basename $<)")

${TOPDIR}/perlsrc/%.pl:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc all,"MAKE","PL")

depop.mak:depop.mak.tmpl ${TOPDIR}/perlsrc/dephandle.pl
	$(call call_exec,${MAKE} --no-print-directory -C . check_dephandle_pl,"CHECKPL","depop.mak")
	$(call call_exec,${PYTHON}  ${TOPDIR}/insertcode -i $<  -p '%PERL_DEP_HANDLE%' -o $@ makestring  ${TOPDIR}/perlsrc/dephandle.pl,"MAK","$(@F)")


clean:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc clean >/dev/null,"CLEAN","PL")
	$(call call_exec,${RM} -f *.tmp,"RM","*.tmp")
	$(call call_exec,${RM} -f ${TEMPLATE_MAKS},"RM","${TEMPLATE_MAKS}")
