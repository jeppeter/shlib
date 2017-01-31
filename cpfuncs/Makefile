
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
	${Q}bash ${TOPDIR}/changefile -i ${TOPDIR}/mountcheck.pl -P cpfuncs.tmpl -o cpfuncs1.tmp -p '%PERL_MOUNTCHECK_STR%' 
	${Q}bash ${TOPDIR}/changefile -i subpath.pl -P cpfuncs1.tmp -o cpfuncs2.tmp -p '%PERL_SUBPATH_STR%'
	${Q}bash ${TOPDIR}/changefile -i shcp.py -P cpfuncs2.tmp -o cpfuncs -p '%PYTHON_SHCP_STR%'

cpin:cpin.tmpl check_dos2unix_pl
	${Q}bash ${TOPDIR}/changefile -i dos2unix.pl -P cpin.tmpl -o cpin -p '%PERL_DOS2UNIX_STR%'

check_dos2unix_pl:dos2unix.pl
	${Q}bash ${TOPDIR}/changefile -i dos2unix.pl -P ${TOPDIR}/echocode.tmpl -o dos2unixpl.tmp -p '%REPLACE_PATTERN%'
	${Q}bash dos2unixpl.tmp > dos2unix.tmp
	${Q}diff -q --strip-trailing-cr -B dos2unix.tmp dos2unix.pl || (echo "not change right for dos2unix.pl" && exit 3)

check_mountcheck_pl:${TOPDIR}/mountcheck.pl
	${Q}bash ${TOPDIR}/changefile -i ${TOPDIR}/mountcheck.pl -P ${TOPDIR}/echocode.tmpl -o echocode.tmp -p '%REPLACE_PATTERN%'
	${Q}bash echocode.tmp > mountcheck.tmp
	${Q}diff -q --strip-trailing-cr -B mountcheck.tmp ${TOPDIR}/mountcheck.pl || (echo "not change right for mountcheck.pl" && exit 3)

check_subpath_pl:subpath.pl
	${Q}bash ${TOPDIR}/changefile -i subpath.pl -P ${TOPDIR}/echocode.tmpl -o subpath_echo.tmp -p '%REPLACE_PATTERN%'
	${Q}bash subpath_echo.tmp > subpath.tmp
	${Q}diff -q --strip-trailing-cr -B subpath.tmp subpath.pl || (echo "not change right for subpath.pl" && exit 3)

check_shcp_py:shcp.py
	${Q}bash ${TOPDIR}/changefile -i shcp.py -P ${TOPDIR}/echocode.tmpl -o shcp_py_echo.tmp -p '%REPLACE_PATTERN%'
	${Q}bash shcp_py_echo.tmp > shcp_py.tmp
	${Q}diff -q --strip-trailing-cr -B shcp_py.tmp shcp.py || (echo "not change right for shcp.py" && exit 3)

clean:
	@${RM} cpfuncs cpin *.tmp