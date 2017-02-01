
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
PYTHON:=$(shell which python)

ifeq (${V},)
Q=@
else
Q=
endif

all:sshsmbmount

sshsmbmount:sshsmbmount.tmpl check_mountcheck_pl
	${Q}${PYTHON} ${TOPDIR}/insertcode -i sshsmbmount.tmpl -o sshsmbmount -p '%PERL_MOUNTCHECK_STR%' bashstring "${TOPDIR}/mountcheck.pl"
	${Q}chmod +x sshsmbmount

check_mountcheck_pl:${TOPDIR}/mountcheck.pl
	${Q}${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -o echocode.tmp -p '%REPLACE_PATTERN%' bashstring "${TOPDIR}/mountcheck.pl"
	${Q}bash echocode.tmp > mountcheck.tmp
	${Q}diff -q --strip-trailing-cr -B mountcheck.tmp ${TOPDIR}/mountcheck.pl || (echo "not change right for mountcheck.pl" && exit 3)

clean:
	${Q}rm -f sshsmbmount *.tmp
