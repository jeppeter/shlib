
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
RM:=$(shell which rm) -rf
BASH:=$(shell which bash)
PYTHON:=$(shell which python)

ifeq (${V},)
Q=@
else
Q=
endif

all:cpfuncs cpin
	${Q}chmod +x cpin cpout
	${Q}${PYTHON} testcp.py -f -v 


cpfuncs:cpfuncs.tmpl check_mountcheck_pl check_subpath_pl check_shcp_py
	${Q}${PYTHON} ${TOPDIR}/insertcode  -i cpfuncs.tmpl  -p '%PERL_MOUNTCHECK_STR%' bashstring ${TOPDIR}/mountcheck.pl | \
		${PYTHON} ${TOPDIR}/insertcode -p  '%PERL_SUBPATH_STR%' bashstring subpath.pl  | \
		${PYTHON} ${TOPDIR}/insertcode -p  '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} ${TOPDIR}/insertcode -p  '%PYTHON_SHCP_STR%' bashstring -o cpfuncs shcp.py

cpin:cpin.tmpl check_dos2unix_pl
	${Q}${PYTHON} ${TOPDIR}/insertcode -i cpin.tmpl -o cpin -p '%PERL_DOS2UNIX_STR%'  bashstring dos2unix.pl

check_dos2unix_pl:dos2unix.pl
	${Q}${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -o dos2unixpl.tmp -p '%REPLACE_PATTERN%' bashstring dos2unix.pl
	${Q}bash dos2unixpl.tmp > dos2unix.tmp
	${Q}diff -q --strip-trailing-cr -B dos2unix.tmp dos2unix.pl || (echo "not change right for dos2unix.pl" && exit 3)

check_mountcheck_pl:${TOPDIR}/mountcheck.pl
	${Q}${PYTHON} ${TOPDIR}/insertcode  -i ${TOPDIR}/echocode.tmpl -o echocode.tmp -p '%REPLACE_PATTERN%' bashstring "${TOPDIR}/mountcheck.pl"
	${Q}bash echocode.tmp > mountcheck.tmp
	${Q}diff -q --strip-trailing-cr -B mountcheck.tmp ${TOPDIR}/mountcheck.pl || (echo "not change right for mountcheck.pl" && exit 3)

check_subpath_pl:subpath.pl
	${Q}${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -o subpath_echo.tmp -p '%REPLACE_PATTERN%' bashstring "subpath.pl"
	${Q}bash subpath_echo.tmp > subpath.tmp
	${Q}diff -q --strip-trailing-cr -B subpath.tmp subpath.pl || (echo "not change right for subpath.pl" && exit 3)

check_shcp_py:shcp.py
	${Q}${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -o shcp_py_echo.tmp -p '%REPLACE_PATTERN%' bashstring shcp.py
	${Q}bash shcp_py_echo.tmp > shcp_py.tmp
	${Q}diff -q --strip-trailing-cr -B shcp_py.tmp shcp.py || (echo "not change right for shcp.py" && exit 3)

clean:
	@${RM} cpfuncs cpin *.tmp