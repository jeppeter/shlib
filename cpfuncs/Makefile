
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
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode  -i cpfuncs.tmpl  -p '%PERL_MOUNTCHECK_STR%' bashstring ${TOPDIR}/mountcheck.pl | \
		${PYTHON} ${TOPDIR}/insertcode -p  '%PERL_SUBPATH_STR%' bashstring subpath.pl  | \
		${PYTHON} ${TOPDIR}/insertcode -p  '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} ${TOPDIR}/insertcode -p  '%PYTHON_SHCP_STR%' bashstring -o cpfuncs shcp.py,"GENSH","cpfuncs")

cpin:cpin.tmpl check_dos2unix_pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i cpin.tmpl -o cpin -p '%PERL_DOS2UNIX_STR%'  bashstring dos2unix.pl,"GENSH","cpin")

check_dos2unix_pl:dos2unix.pl
	$(call call_exec,(${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' \
		bashstring dos2unix.pl | ${BASH} | ${DIFF} -B - dos2unix.pl ) || \
		(${ECHO} "can not make dos2unix.pl right" >&2 ; exit 3),\
		"CHECK","dos2unix.pl")

check_mountcheck_pl:${TOPDIR}/mountcheck.pl
	$(call call_exec,($(PYTHON) ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' bashstring "${TOPDIR}/mountcheck.pl" | \
			${BASH} | ${DIFF} -B - ${TOPDIR}/mountcheck.pl) || \
			(${ECHO} "can not change ${TOPDIR}/mountcheck.pl ok" ; exit 3),"CHECK","mountcheck.pl")

check_subpath_pl:subpath.pl
	$(call call_exec,($(PYTHON) ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' bashstring "${CURDIR}/subpath.pl" | \
			${BASH} | ${DIFF} -B - ${CURDIR}/subpath.pl) || \
			(${ECHO} "can not change ${CURDIR}/subpath.pl ok" ; exit 3),"CHECK","subpath.pl")

check_shcp_py:shcp.py
	$(call call_exec,($(PYTHON) ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' bashstring "${CURDIR}/shcp.py" | \
			${BASH} | ${DIFF} -B - ${CURDIR}/shcp.py) || \
			(${ECHO} "can not change ${CURDIR}/shcp.py ok" ; exit 3),"CHECK","shcp.py")

clean:
	$(call call_exec,$(RM) -rf cpin cpfuncs,"RM","cpin cpfuncs")