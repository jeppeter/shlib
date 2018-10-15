
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
CURDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' .)

ifeq (${V},)
Q=@
else
Q=
endif

include ${TOPDIR}/basedef.mak

all:initcp

initcp:initcp.tmpl check_libs
	$(call call_exec,${PYTHON} -m insertcode -i initcp.tmpl  -p '%DEBUGSH_CODE%'  bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} -m insertcode -p '%PKGSH_CODE%' bashinsert "${TOPDIR}/libs/pkgsh" | \
		${PYTHON} -m insertcode -p '%RUNSH_CODE%' bashinsert "${TOPDIR}/libs/runsh" | \
		${PYTHON} -m insertcode -o initcp -p '%DEFINESH_CODE%' bashinsert "${TOPDIR}/libs/definesh",\
		"GENSH",$@)
	$(call call_exec,${CHX} ${CURDIR}/initcp,"CHX",$@)

check_libs:${TOPDIR}/libs/debugsh ${TOPDIR}/libs/definesh ${TOPDIR}/libs/runsh ${TOPDIR}/libs/pkgsh

${TOPDIR}/libs/%:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/libs all,"MAKE","SH")

clean:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/libs clean,"CLEAN","SH")
	$(call call_exec,${RM} -f initcp,"RM",initcp)
