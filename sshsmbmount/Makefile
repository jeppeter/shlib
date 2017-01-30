
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)

ifeq (${V},)
Q=@
else
Q=
endif

all:sshsmbmount

sshsmbmount:sshsmbmount.tmpl check_mountcheck_pl
	${Q}bash ${TOPDIR}/changefile -i ${TOPDIR}/mountcheck.pl -P sshsmbmount.tmpl -o sshsmbmount -p '%PERL_MOUNTCHECK_STR%'
	${Q}chmod +x sshsmbmount

check_mountcheck_pl:${TOPDIR}/mountcheck.pl
	${Q}bash ${TOPDIR}/changefile -i ${TOPDIR}/mountcheck.pl -P ${TOPDIR}/echocode.tmpl -o echocode.tmp -p '%REPLACE_PATTERN%'
	${Q}bash echocode.tmp > mountcheck.tmp
	${Q}diff -q --strip-trailing-cr -B mountcheck.tmp ${TOPDIR}/mountcheck.pl || (echo "not change right for mountcheck.pl" && exit 3)

clean:
	${Q}rm -f sshsmbmount *.tmp
