
TOPDIR:=$(shell perl -e 'use Cwd "abs_path";print abs_path(shift);' ..)
CURDIR:=$(shell perl -e 'use Cwd "abs_path";print abs_path(shift);' .)

ifeq (${V},)
Q=@
else
Q=
endif


include ${TOPDIR}/basedef.mak


all:makelib.mak

makelib.mak:basedef.mak fileop.mak varop.mak exec.mak  depop.mak makelib.mak.tmpl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i makelib.mak.tmpl -p '%BASEDEF_MAK%' bashinsert ${CURDIR}/basedef.mak |\
		  ${PYTHON} ${TOPDIR}/insertcode -p '%VAROP_MAK%' bashinsert ${CURDIR}/varop.mak | \
		  ${PYTHON} ${TOPDIR}/insertcode -p '%EXEC_MAK%' bashinsert ${CURDIR}/exec.mak | \
		  ${PYTHON} ${TOPDIR}/insertcode -p '%FILEOP_MAK%' bashinsert ${CURDIR}/fileop.mak | \
		  ${PYTHON} ${TOPDIR}/insertcode -p '%DEPOP_MAK%' -o $@ bashinsert ${CURDIR}/depop.mak,"MAK","$(@F)")

fileop.mak:fileop.mak.tmpl check_readlink_pl check_exename_pl check_toobj_pl check_filterop_pl check_basename_pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode  -i $< -p '%PERL_READLINK_STR%' makestring ${TOPDIR}/perlsrc/readlink.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_EXENAME_STR%' makestring ${TOPDIR}/perlsrc/exename.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_TOOBJ_STR%' makestring ${TOPDIR}/perlsrc/toobj.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_FILTEROP_STR%' makestring ${TOPDIR}/perlsrc/filterop.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_BASENAME_STR%' -o $@ makestring ${TOPDIR}/perlsrc/basename.pl,"MAK","$(@F)")

check_readlink_pl:${TOPDIR}/perlsrc/readlink.pl




varop.mak:varop.mak.tmpl check_shortname_pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i $< -p '%PERL_SHORTNAME_STR%' -o $@ makestring ${TOPDIR}/perlsrc/shortname.pl,"MAK","$(@F)")

check_shortname_pl:${TOPDIR}/perlsrc/shortname.pl

check_exename_pl:${TOPDIR}/perlsrc/exename.pl

check_toobj_pl:${TOPDIR}/perlsrc/toobj.pl

check_filterop_pl:${TOPDIR}/perlsrc/filterop.pl

check_dephandle_pl:${TOPDIR}/perlsrc/dephandle.pl

check_%_pl:${TOPDIR}/perlsrc/%.pl
	$(call call_exec,(${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.tmpl -p '%REPLACE_PATTERN%' \
		bashstring $< | ${BASH} | ${DIFF} -B - $< ) || \
		(${ECHO} "can not make $< right" >&2 ; exit 3),\
		"CHECK","$(basename $<)")

${TOPDIR}/perlsrc/%.pl:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc all,"MAKE","PL")

depop.mak:depop.mak.tmpl check_dephandle_pl
	$(call call_exec,${PYTHON}  ${TOPDIR}/insertcode -i $<  -p '%PERL_DEP_HANDLE%' -o $@ makestring  ${TOPDIR}/perlsrc/dephandle.pl,"MAK","$(@F)")


clean:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc clean >/dev/null,"CLEAN","PL")
	$(call call_exec,${RM} -f *.tmp,"RM","*.tmp")
	$(call call_exec,${RM} -f fileop.mak varop.mak dependsop.mak,"RM","fileop.mak varop.mak dependsop.mak")
