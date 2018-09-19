
TOPDIR:=$(shell perl -e 'use Cwd "abs_path";foreach(@ARGV) { print abs_path($$_)."\n";}' .)

ifeq (${V},)
Q=@
MAKE_VERBOSE=--no-print-directory
else
Q=
MAKE_VERBOSE=
endif

include ${TOPDIR}/basedef.mak

subdirs=sshsmbmount cpfuncs mkcode initcp encsh makelib
ifeq (${OSNAME},darwin)
subdirs+= macos
endif



define call_make_dir_mode
$(call call_exec_directly,${MAKE} -C $(1) ${MAKE_VERBOSE} $(2) >/dev/null || ( ${ECHO} "can not run $(1)" >&2 ; exit 3 ),"MAKE","[$(1)]$(2)");
endef


all:make_libs
	${Q}$(foreach curdir,${subdirs},$(call call_make_dir_mode,${curdir},all))

make_libs:
	${Q}$(call call_make_dir_mode,libs,all)

clean_libs:
	${Q}$(call call_make_dir_mode,libs,clean)

clean:clean_libs
	${Q}$(foreach curdir,${subdirs},$(call call_make_dir_mode,${curdir},clean))
