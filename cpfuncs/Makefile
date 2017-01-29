
RM:=$(shell which rm)
BASH:=$(shell which bash)

all:cpfuncs

cpfuncs:cpfuncs.tmpl check_mountcheck_pl
	${QUIET}bash ${TOPDIR}/changefile -i ${TOPDIR}/mountcheck.pl -P cpfuncs.tmpl -o cpfuncs -p '%PERL_MOUNTCHECK_STR%'

check_mountcheck_pl:${TOPDIR}/mountcheck.pl
	${QUIET}bash ${TOPDIR}/changefile -i ${TOPDIR}/mountcheck.pl -P ${TOPDIR}/echocode.tmpl -o mountcheck.tmp -p '%REPLACE_PATTERN%'
	${QUIET}bash mountcheck.tmp > mountcheck.tmp
	${QUIET}diff -q -B -Z mountcheck.tmp ${TOPDIR}/mountcheck.pl || (echo "not change right for mountcheck.pl" && exit 3)

clean:
	@${RM} cpfuncs