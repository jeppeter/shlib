
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
CURDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' .)

ifeq (${V},)
Q=@
else
Q=
endif

include ${TOPDIR}/basedef.mak

all:xbuild

xbuild:xbuild.tmpl check_libs
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i xbuild.tmpl  -p '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} ${TOPDIR}/insertcode -o xbuild -p '%DEPENDSH_CODE%' bashinsert "${TOPDIR}/libs/dependsh",\
		"GENSH",$@)
	$(call call_exec,${CHX} ${CURDIR}/xbuild,"CHX",$@)

check_libs:${TOPDIR}/libs/dependsh ${TOPDIR}/libs/debugsh

${TOPDIR}/libs/%:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/libs all,"MAKE","SH")

clean:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/libs clean,"CLEAN","SH")
	$(call call_exec,${RM} -f xbuild,"RM",xbuild)
