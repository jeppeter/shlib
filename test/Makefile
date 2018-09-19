
ifeq (${V},)
Q=@
else
Q=
endif

include ../basedef.mak

TOPDIR:=$(shell perl -e "use strict;use Cwd \"abs_path\";print abs_path(shift);" ../)

all:echotest.sh


echotest.sh:echotest.sh.tmpl ${TOPDIR}/libs/definesh ${TOPDIR}/libs/debugsh
	$(call call_exec,${PYTHON} -m insertcode -i $< -p '%DEFINESH_CODE%' bashinsert ${TOPDIR}/libs/definesh | \
			${PYTHON} -m insertcode -p '%DEBUGSH_CODE%' -o $@ bashinsert ${TOPDIR}/libs/debugsh,"GENSH","$(@F)")

clean:
	$(call call_exec,${RM} -f echotest.sh,"RM","echotest.sh")