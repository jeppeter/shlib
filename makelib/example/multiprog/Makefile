
include ../../makelib.mak

TOPDIR:=$(call readlink_f,.)

osname:=$(call get_osname)

ifneq ($(patsubst cygwin_%,%,${osname}),${osname})
exesuffix:=.exe
else
exesuffix:=
endif

ipxeload_elf_DEPS += pre_ipxeload_elf
ipxeload_elf_POST += post_ipxeload_elf
ipxeload_elf_DEPS_CLEAN = clean_pre_ipxeload_elf
ipxeload_elf_SRCS = a.c 
ipxeload_elf_SRCS += jjk.c
ipxeload_elf_SRCS += k.cpp
ipxeload_elf_SRCS += ia.S ib.S
ipxeload_elf_SRCS += f.link.c
f_link_c_SRC = f.c
ipxeload_elf_SRCS += ic.link.S ibb.link.S
ic_link_S_SRC = ic.S
ibb_link_S_SRC = ibb.S
ipxeload_elf_SRCS += j.link.cpp
j_link_cpp_SRC = j.cpp
INCLUDE_FLAGS = -I${TOPDIR}/inc
ipxeload_elf_CFLAGS = -Wall -DCFILE=1 ${INCLUDE_FLAGS}
#ipxeload_elf_CPPFLAGS = -Wall -DCPPFILE=1 ${INCLUDE_FLAGS}
ipxeload_elf_LDFLAGS = -Wall -DLDFLILE=1 ${INCLUDE_FLAGS}
#ipxeload_elf_ASFLAGS = -Wall -DASFILE=1 ${INCLUDE_FLAGS}
d_link_c_SRC = d.c
f_link_cpp_SRC = g.cpp
a_c_DEPS_USER = keygen.c

main_SRCS = main.c b.c c.c
main_CFLAGS = -Wall -DMAIN_CFILE=1 ${INCLUDE_FLAGS}
main_CPPFLAGS = -Wall -DMAIN_CPPFILE=1 ${INCLUDE_FLAGS}
main_LDFLAGS = -Wall -DMAIN_LDFLILE=1 ${INCLUDE_FLAGS}
main_ASFLAGS = -Wall -DMAIN_ASFILE=1 ${INCLUDE_FLAGS}
MAKEDEPS += ${TOPDIR}/Makefile

#ipxeload_elf_LD = ${TOPDIR}/gpp.sh
#ipxeload_elf_GCC = ${TOPDIR}/gcc.sh
#ipxeload_elf_GPP = ${TOPDIR}/gpp.sh
#ipxeload_elf_GAS = ${TOPDIR}/gas.sh

all:post_ipxeload_elf main${exesuffix}
#$(call call_all_exe,ipxeload_elf main)

post_ipxeload_elf: ${TOPDIR}/ipxeload.elf${exesuffix}
	$(call call_exec,${TRUE},"POST","ipxeload.elf${exesuffix}")

pre_ipxeload_elf:
	$(call call_exec,${TRUE},"PRE","ipxeload.elf${exesuffix}")

clean_pre_ipxeload_elf:
	$(call call_exec,${TRUE},"CLEANPRE","ipxeload.elf${exesuffix}")

clean_post_ipxeload_elf:clean_ipxeload_elf
	$(call call_exec,${TRUE},"CLEANPOST","ipxeload.elf${exesuffix}")	

keygen.c:
	$(call call_exec,${TOUCH} $@,"TOUCH","keygen.c")

$(eval $(call simple_makefile_exe_whole,${TOPDIR}/ipxeload.elf${exesuffix} main${exesuffix}))
#$(call foreach_makefile_exe_whole,ipxeload_elf main)

clean:clean_post_ipxeload_elf clean_main
	$(call call_exec,${RM} -f keygen.c,"RM","keygen.c")
#$(call call_clean_exe,ipxeload_elf main)
