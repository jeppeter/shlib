
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

TEMPLATE_MAKS = basedef.mak  fileop.mak varop.mak depop.mak makelib.mak exec.mak

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
	$(call call_exec,${MAKE} --no-print-directory -C . check_pl_readlink_mak check_pl_exename_mak check_pl_toobj_mak  check_pl_filterop_mak check_pl_basename_mak check_pl_getdep_mak check_pl_getsoname_mak,"CHECKPL","fileop.mak")
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode  -i $< -p '%PERL_READLINK_STR%' makeperl ${TOPDIR}/perlsrc/readlink.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_EXENAME_STR%' makeperl ${TOPDIR}/perlsrc/exename.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_TOOBJ_STR%' makeperl ${TOPDIR}/perlsrc/toobj.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_FILTEROP_STR%' makeperl ${TOPDIR}/perlsrc/filterop.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_GETDEP_STR%' makeperl ${TOPDIR}/perlsrc/getdep.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_GETSONAME_STR%' makeperl ${TOPDIR}/perlsrc/getsoname.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_BASENAME_STR%' -o $@ makeperl ${TOPDIR}/perlsrc/basename.pl,"MAK","$(@F)")

exec.mak:exec.mak.tmpl ${TOPDIR}/pysrc/osname.py
	$(call call_exec,${MAKE} --no-print-directory -C ${CURDIR} check_py_osname_mak,"CHECKPY","exec.mak")
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i $< -p '%PYTHON_OSNAME_STR%' -o $@ makepython ${TOPDIR}/pysrc/osname.py,"MAK","$(@F)")

varop.mak:varop.mak.tmpl ${TOPDIR}/perlsrc/shortname.pl ${TOPDIR}/perlsrc/defval.pl
	$(call call_exec,${MAKE} --no-print-directory -C . check_pl_shortname_mak check_pl_defval_mak,"CHECKPL","varop.mak")
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i $< -p '%PERL_SHORTNAME_STR%'  makeperl ${TOPDIR}/perlsrc/shortname.pl | \
		${PYTHON} ${TOPDIR}/insertcode -p '%PERL_DEFVAL_STR%' -o $@ makeperl ${TOPDIR}/perlsrc/defval.pl,"MAK","$(@F)")


check_pl_readlink_mak:${TOPDIR}/perlsrc/readlink.pl

check_pl_exename_mak:${TOPDIR}/perlsrc/exename.pl

check_pl_toobj_mak:${TOPDIR}/perlsrc/toobj.pl

check_pl_filterop_mak:${TOPDIR}/perlsrc/filterop.pl

check_pl_getdep_mak:${TOPDIR}/perlsrc/getdep.pl

check_pl_getsoname_mak:${TOPDIR}/perlsrc/getsoname.pl

check_pl_basename_mak:${TOPDIR}/perlsrc/basename.pl

check_pl_shortname_mak:${TOPDIR}/perlsrc/shortname.pl

check_pl_defval_mak:${TOPDIR}/perlsrc/defval.pl

check_pl_%_mak:${TOPDIR}/perlsrc/%.pl
	$(call call_exec,(${PYTHON} ${TOPDIR}/insertcode -i  ${TOPDIR}/echocode_perl.mak.tmpl -p '%REPLACE_PATTERN%' \
		makeperl $< | ${MAKE} -f /dev/stdin | ${DIFF} - $< ) || \
		(${ECHO} "can not make $< right" >&2 ; exit 3),"CHECK","$(<F)")

check_py_osname_mak:${TOPDIR}/pysrc/osname.py

check_py_%_mak:${TOPDIR}/pysrc/%.py
	$(call call_exec,(${PYTHON} ${TOPDIR}/insertcode -i  ${TOPDIR}/echocode_python.mak.tmpl -p '%REPLACE_PATTERN%' \
		makepython $< | ${MAKE} -f /dev/stdin | ${DIFF} - $< ) || \
		(${ECHO} "can not make $< right" >&2 ; exit 3),"CHECK","$(<F)")

${TOPDIR}/perlsrc/%.pl:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc all,"MAKE","PL")

depop.mak:depop.mak.tmpl ${TOPDIR}/perlsrc/dephandle.pl
	$(call call_exec,${MAKE} --no-print-directory -C . check_pl_dephandle_mak,"CHECKPL","depop.mak")
	$(call call_exec,${PYTHON}  ${TOPDIR}/insertcode -i $<  -p '%PERL_DEP_HANDLE%' -o $@ makeperl  ${TOPDIR}/perlsrc/dephandle.pl,"MAK","$(@F)")


clean:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc clean >/dev/null,"CLEAN","PL")
	$(call call_exec,${RM} -f *.tmp,"RM","*.tmp")
	$(call call_exec,${RM} -f ${TEMPLATE_MAKS},"RM","${TEMPLATE_MAKS}")
