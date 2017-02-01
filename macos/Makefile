
TOPDIR:=$(shell perl -e 'use Cwd "abs_path"; print abs_path(shift);' ../)
PYTHON:=$(shell which python)

ifeq (${V},)
Q=@
else
Q=
endif

all:xbuild

xbuild:xbuild.tmpl check_libs
	${Q}${PYTHON} ${TOPDIR}/insertcode -i xbuild.tmpl  -p '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} ${TOPDIR}/insertcode -o xbuild -p '%DEPENDSH_CODE%' bashinsert "${TOPDIR}/libs/dependsh" 
	${Q}chmod +x xbuild

check_libs:

clean:
	${Q}rm -f xbuild *.tmp
