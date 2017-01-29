
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
RM:=$(shell which rm) -rf
BASH:=$(shell which bash)

ifeq (${V},)
Q=@
else
Q=
endif

all:cpfuncs cpin

cpfuncs:cpfuncs.tmpl check_mountcheck_pl
	${Q}bash ${TOPDIR}/changefile -i ${TOPDIR}/mountcheck.pl -P cpfuncs.tmpl -o cpfuncs -p '%PERL_MOUNTCHECK_STR%'

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

clean:
	@${RM} cpfuncs cpin