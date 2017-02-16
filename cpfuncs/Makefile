
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
CURDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' .)

ifeq (${V},)
Q=@
else
Q=
endif

include ${TOPDIR}/basedef.mak

all:cpfuncs cpin
	$(call call_exec,${CHX} cpin cpout,"CHX","cpin cpout")
	$(call call_exec,${PYTHON} testcp.py -f >/dev/null,"TEST","cpin cpout")


cpfuncs:cpfuncs.tmpl check_mountcheck_pl check_subpath_pl check_shcp_py
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode  -i cpfuncs.tmpl  -p '%PERL_MOUNTCHECK_STR%' bashstring ${TOPDIR}/perlsrc/mountcheck.pl | \
		${PYTHON} ${TOPDIR}/insertcode -p  '%PERL_SUBPATH_STR%' bashstring ${TOPDIR}/perlsrc/subpath.pl  | \
		${PYTHON} ${TOPDIR}/insertcode -p  '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} ${TOPDIR}/insertcode -p  '%PYTHON_SHCP_STR%' bashstring -o cpfuncs ${TOPDIR}/pysrc/shcp.py,"GENSH","cpfuncs")

cpin:cpin.tmpl check_dos2unix_pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i cpin.tmpl -o cpin -p '%PERL_DOS2UNIX_STR%'  bashstring ${TOPDIR}/perlsrc/dos2unix.pl,"GENSH","cpin")

check_dos2unix_pl:${TOPDIR}/perlsrc/dos2unix.pl

check_mountcheck_pl:${TOPDIR}/perlsrc/mountcheck.pl

check_subpath_pl:${TOPDIR}/perlsrc/subpath.pl

check_shcp_py:${TOPDIR}/pysrc/shcp.py

check_%_pl:${TOPDIR}/perlsrc/%.pl
	$(call call_exec,(${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' \
		bashstring $< | ${BASH} | ${DIFF} -B - $< ) || \
		(${ECHO} "can not make $< right" >&2 ; exit 3),\
		"CHECK","$(basename $<)")

${TOPDIR}/perlsrc/%.pl:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc all,"MAKE","PL")

${TOPDIR}/pysrc/*.py:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/pysrc all,"MAKE","PY")

check_%_py:${TOPDIR}/pysrc/%.py
	$(call call_exec,($(PYTHON) ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' bashstring $< | \
			${BASH} | ${DIFF} -B - $< ) || \
			(${ECHO} "can not change $< ok" ; exit 3),"CHECK","$(basename $<)")


clean:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc clean,"CLEAN","PL")
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/pysrc clean,"CLEAN","PY")
	$(call call_exec,$(RM) -rf cpin cpfuncs,"RM","cpin cpfuncs")