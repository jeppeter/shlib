
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
CURDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' .)



ifeq (${V},)
Q=@
else
Q=
endif

include ${TOPDIR}/basedef.mak


all:sshsmbmount

sshsmbmount:sshsmbmount.tmpl check_mountcheck_pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i sshsmbmount.tmpl -o sshsmbmount -p '%PERL_MOUNTCHECK_STR%' bashstring ${TOPDIR}/perlsrc/mountcheck.pl,"GENSH","$(@F)")
	$(call call_exec,${CHX} sshsmbmount,"CHX","$(@F)")

check_mountcheck_pl:${TOPDIR}/perlsrc/mountcheck.pl

check_%_pl:${TOPDIR}/perlsrc/%.pl
	$(call call_exec,(${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' \
		bashstring $< | ${BASH} | ${DIFF} -B - $< ) || \
		(${ECHO} "can not make $< right" >&2 ; exit 3),\
		"CHECK","$(basename $<)")

${TOPDIR}/perlsrc/%.pl:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc all,"MAKE","PL")


clean:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc clean >/dev/null,"CLEAN","PL")
	$(call call_exec,${RM} -f sshsmbmount *.tmp,"RM","sshsmbmount *.tmp")
