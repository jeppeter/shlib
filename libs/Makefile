
TOPDIR:=$(shell perl -e 'use Cwd "abs_path";foreach(@ARGV) { print abs_path($$_)."\n";}' ../)

ifeq (${V},)
Q=@
else
Q=
endif

include ${TOPDIR}/basedef.mak

CURDIR:=$(shell perl -e 'use Cwd "abs_path";foreach(@ARGV) { print abs_path($$_)."\n";}' ./)




all:perlcomsh

perlcomsh:perlcomsh.tmpl check_readlink_pl check_basename_pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i perlcomsh.tmpl  -p '%PERL_READLINK_STR%' bashstring ${TOPDIR}/perlsrc/readlink.pl | \
		 ${PYTHON} ${TOPDIR}/insertcode -p '%PERL_BASENAME_STR%' bashstring -o $@ "${TOPDIR}/perlsrc/basename.pl" , \
		 "GENSH","$@" )
	$(call call_exec,${CHX} $@,"CHX",$@)

check_readlink_pl:${TOPDIR}/perlsrc/readlink.pl

check_basename_pl:${TOPDIR}/perlsrc/basename.pl

check_%_pl:${TOPDIR}/perlsrc/%.pl
	$(call call_exec,(${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' \
		bashstring $< | ${BASH} | ${DIFF} -B - $< ) || \
		(${ECHO} "can not make $< right" >&2 ; exit 3),\
		"CHECK","$(basename $<)")

${TOPDIR}/perlsrc/%.pl:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc all,"MAKE","PL")


clean:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc clean,"CLEAN","PL")
	$(call call_exec,${RM} -f perlcomsh,"RM",perlcomsh)
	$(call call_exec,${RM} -f *.tmp,"RM","*.tmp")
