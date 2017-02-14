
TOPDIR:=$(shell perl -e 'use Cwd "abs_path";foreach (@ARGV){print $$_."\n";}' ..)
CURDIR:=$(shell perl -e 'use Cwd "abs_path";foreach (@ARGV){print $$_."\n";}' .)

ifeq (${V},)
Q=@
else
Q=
endif


include ${TOPDIR}/basedef.mak


all:makelib.mak


makelib.mak:basedef.mak varop.mak exec.mak fileop.mak depop.mak makelib.mak.tmpl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i makelib.mak.tmpl -p '%BASEDEF_MAK%' bashinsert ${CURDIR}/basedef.mak |\
		  ${PYTHON} ${TOPDIR}/insertcode -p '%VAROP_MAK%' bashinsert ${CURDIR}/varop.mak | \
		  ${PYTHON} ${TOPDIR}/insertcode -p '%EXEC_MAK%' bashinsert ${CURDIR}/exec.mak | \
		  ${PYTHON} ${TOPDIR}/insertcode -p '%FILEOP_MAK%' bashinsert ${CURDIR}/fileop.mak | \
		  ${PYTHON} ${TOPDIR}/insertcode -p '%DEPOP_MAK%' -o $@ bashinsert ${CURDIR}/depop.mak,"MAK","$(@F)")

fileop.mak:fileop.mak.tmpl check_readlink_pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode  -i $< -p '%PERL_READLINK_STR%' makestring ${TOPDIR}/readlink.pl | \
			${PYTHON} ${TOPDIR}/insertcode -p '%PERL_BASENAME_STR%' -o $@ makestring ${TOPDIR}/basename.pl,"MAK","$(@F)")

check_readlink_pl:${TOPDIR}/readlink.pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.mak.tmpl -o $@.mak.tmp makestring ${TOPDIR}/readlink.pl,"TMPMAK","$@.mak.tmp" )
	$(call call_exec,${MAKE} --no-print-directory -f $@.mak.tmp >$@.1.tmp,"MAKE","$@.1.tmp")
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode  -o $@.2.tmp makeformat ${TOPDIR}/readlink.pl,"TMPMAK","$@.2.tmp")
	$(call call_exec,${DIFF} -B $@.1.tmp $@.2.tmp  ||  (${ECHO} "$@ error" >&2; exit 3),"CHK","$@")

varop.mak:varop.mak.tmpl check_shortname_pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i $< -p '%PERL_SHORTNAME_STR%' -o $@ makestring ${TOPDIR}/shortname.pl,"MAK","$(@F)")

check_shortname_pl:${TOPDIR}/shortname.pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.mak.tmpl -o $@.mak.tmp makestring ${TOPDIR}/shortname.pl,"TMPMAK","$@.mak.tmp" )
	$(call call_exec,${MAKE} --no-print-directory -f $@.mak.tmp >$@.1.tmp,"MAKE","$@.1.tmp")
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode  -o $@.2.tmp makeformat ${TOPDIR}/shortname.pl,"TMPMAK","$@.2.tmp")
	$(call call_exec,${DIFF} -B $@.1.tmp $@.2.tmp  ||  (${ECHO} "$@ error" >&2; exit 3),"CHK","$@")

depop.mak:depop.mak.tmpl check_dep_handle_pl
	$(call call_exec,${PYTHON}  ${TOPDIR}/insertcode -i $<  -p '%PERL_DEP_HANDLE%' -o $@ makestring  ${CURDIR}/dephandle.pl,"MAK","$(@F)")

check_dep_handle_pl:${CURDIR}/dephandle.pl
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode -i ${TOPDIR}/echocode.mak.tmpl -o $@.mak.tmp makestring ${CURDIR}/dephandle.pl,"TMPMAK","$@.mak.tmp" )
	$(call call_exec,${MAKE} --no-print-directory -f $@.mak.tmp >$@.1.tmp,"MAKE","$@.1.tmp")
	$(call call_exec,${PYTHON} ${TOPDIR}/insertcode  -o $@.2.tmp makeformat ${CURDIR}/dephandle.pl,"TMPMAK","$@.2.tmp")
	$(call call_exec,${DIFF} -B $@.1.tmp $@.2.tmp  ||  (${ECHO} "$@ error" >&2; exit 3),"CHK","$@")

clean:
	$(call call_exec,${RM} -f *.tmp,"RM","*.tmp")
	$(call call_exec,${RM} -f fileop.mak varop.mak dependsop.mak,"RM","fileop.mak varop.mak dependsop.mak")
