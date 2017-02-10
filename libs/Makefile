
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
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i perlcomsh.tmpl  -p '%PERL_READLINK_STR%' bashstring "${CURDIR}/readlink.pl" | \
		 ${PYTHON} ${TOPDIR}/insertcode -p '%PERL_BASENAME_STR%' bashstring -o $@ "${CURDIR}/basename.pl" , \
		 "GENSH","$@" )
	$(call call_exec,${CHX} $@,"CHX",$@)

check_readlink_pl:readlink.pl
	$(call call_exec, ( ${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%'  bashstring "${CURDIR}/readlink.pl" | ${BASH} | ${DIFF} -B - ${CURDIR}/readlink.pl ) || (${ECHO} "can not change readlink.pl ok" >&2; exit 3),"CHECK" ,"readlink.pl")

check_basename_pl:basename.pl
	$(call call_exec, ( ${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%'  bashstring "${CURDIR}/basename.pl" | ${BASH} | ${DIFF} -B - ${CURDIR}/basename.pl ) || (${ECHO} "can not change basename.pl ok" >&2; exit 3),"CHECK" ,"basename.pl")

clean:
	$(call call_exec,${RM} -f perlcomsh,"RM",perlcomsh)
	$(call call_exec,${RM} -f *.tmp,"RM","*.tmp")
