
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
CURDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' .)
PYTHON:=$(shell which python)

ifeq (${V},)
Q=@
else
Q=
endif

all:mkcode

mkcode:mkcode.tmpl check_libs
	${Q}${PYTHON} ${TOPDIR}/insertcode -i mkcode.tmpl  -p '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} ${TOPDIR}/insertcode -p '%DEFINESH_CODE%' bashinsert "${TOPDIR}/libs/definesh" | \
		${PYTHON} ${TOPDIR}/insertcode -p '%PERL_BASE_NAME%' bashstring "${CURDIR}/bname.pl" | \
		${PYTHON} ${TOPDIR}/insertcode -o mkcode -p '%DEPENDSH_CODE%' bashinsert "${TOPDIR}/libs/dependsh" 
	${Q}chmod +x mkcode

check_libs:

clean:
	${Q}rm -f mkcode *.tmp
