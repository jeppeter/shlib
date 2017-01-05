
TOPDIR:=$(shell pwd)

subdirs:=sshsmbmount cpfuncs

ifeq (${V},)
QUIET=@
else
QUIET=
endif

export TOPDIR QUIET

all:
	${QUIET}for _i in ${subdirs} ; do ${MAKE} -C $$_i $@ ; if [ $$? -ne 0 ] ; then echo "can not make [$$_i]"; exit 3 ;fi ; done


clean:
	${QUIET}for _i in ${subdirs} ; do ${MAKE} -C $$_i $@ ; if [ $$? -ne 0 ] ; then echo "can not make [$$_i]"; exit 3 ;fi ; done