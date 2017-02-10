
TOPDIR:=$(shell pwd)
OSNAME:=$(shell uname -s | tr [:upper:] [:lower:])

subdirs=sshsmbmount cpfuncs mkcode
ifeq (${OSNAME},darwin)
subdirs+= macos
endif

ifeq (${V},)
Q=@
else
Q=
endif

export TOPDIR QUIET

all:
	${Q}for _i in ${subdirs} ; do ${MAKE} -C $$_i $@ ; if [ $$? -ne 0 ] ; then echo "can not make [$$_i]"; exit 3 ;fi ; done


clean:
	${Q}for _i in ${subdirs} ; do ${MAKE} -C $$_i $@ ; if [ $$? -ne 0 ] ; then echo "can not make [$$_i]"; exit 3 ;fi ; done