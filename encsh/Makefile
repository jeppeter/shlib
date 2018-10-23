
TOPDIR=../
ALLFILES=makeinst.sh init.sh encboot.sh.tmpl

include $(TOPDIR)/basedef.mak


all:${ALLFILES}


makeinst.sh:makeinst.sh.tmpl  check_libs
	$(call call_exec,${PYTHON} -m insertcode -i $<  -p '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} -m insertcode -p '%DEFINESH_CODE%' bashinsert "${TOPDIR}/libs/definesh" | \
		${PYTHON} -m insertcode -p '%PERL_BASE_NAME%' bashstring "${TOPDIR}/perlsrc/basename.pl" | \
		${PYTHON} -m insertcode -p '%PYTHON_MD5_STR%' bashstring ${TOPDIR}/pysrc/calcmd5.py | \
		${PYTHON} -m insertcode -p '%RUNSH_CODE%' bashinsert "${TOPDIR}/libs/runsh" | \
		${PYTHON} -m insertcode -o $@ -p '%DEPENDSH_CODE%' bashinsert "${TOPDIR}/libs/dependsh","GENSH",$@)
	$(call call_exec,${CHX} $@,"CHX",$@)

init.sh:init.sh.tmpl  check_libs
	$(call call_exec,${PYTHON} -m insertcode -i $<  -p '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} -m insertcode -p '%DEFINESH_CODE%' bashinsert "${TOPDIR}/libs/definesh" | \
		${PYTHON} -m insertcode -p '%PERL_BASE_NAME%' bashstring "${TOPDIR}/perlsrc/basename.pl" | \
		${PYTHON} -m insertcode -p '%PYTHON_MD5_STR%' bashstring ${TOPDIR}/pysrc/calcmd5.py | \
		${PYTHON} -m insertcode -p '%RUNSH_CODE%' bashinsert "${TOPDIR}/libs/runsh" | \
		${PYTHON} -m insertcode -p '%PKGSH_CODE%' bashinsert "${TOPDIR}/libs/pkgsh" | \
		${PYTHON} -m insertcode -o $@ -p '%DEPENDSH_CODE%' bashinsert "${TOPDIR}/libs/dependsh","GENSH",$@)
	$(call call_exec,${CHX} $@,"CHX",$@)

encboot.sh.tmpl:encboot.sh.tmpl.tmpl check_libs
	$(call call_exec,${PYTHON} -m insertcode -i $<  -p '%DEBUGSH_CODE%' bashinsert "${TOPDIR}/libs/debugsh" | \
		${PYTHON} -m insertcode -p '%DEFINESH_CODE%' bashinsert "${TOPDIR}/libs/definesh" | \
		${PYTHON} -m insertcode -p '%RUNSH_CODE%' bashinsert "${TOPDIR}/libs/runsh" | \
		${PYTHON} -m insertcode -o $@ -p '%DEPENDSH_CODE%' bashinsert "${TOPDIR}/libs/dependsh","GENSH",$@)
	$(call call_exec,${CHX} $@,"CHX",$@)

check_libs:check_calcmd5_py check_basename_pl

check_calcmd5_py:${TOPDIR}/pysrc/calcmd5.py

check_basename_pl:${TOPDIR}/perlsrc/basename.pl

check_%_py:${TOPDIR}/pysrc/%.py
	$(call call_exec,${PYTHON} -m insertcode -i ${TOPDIR}/echocode.tmpl bashstring $< | ${BASH} | ${DIFF} - $<,"CHECK","$(<F)")


check_%_pl:${TOPDIR}/perlsrc/%.pl
	$(call call_exec,${PYTHON} -m insertcode -i ${TOPDIR}/echocode.tmpl bashstring $< | ${BASH} | ${DIFF} - $<,"CHECK","$(<F)")

${TOPDIR}/perlsrc/%.pl:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc all,"MAKE","PL")

clean_pl:
	$(call call_exec,${MAKE} --no-print-directory -C ${TOPDIR}/perlsrc clean,"CLEAN","PL")

clean:clean_pl
	$(call call_exec,rm -f ${ALLFILES} *.tmp,"RM","${ALLFILES} *.tmp")



