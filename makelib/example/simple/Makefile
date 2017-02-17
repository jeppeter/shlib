
include ../../makelib.mak

TOPDIR:=$(call readlink_f,.)

setjjk_DEPS = pre_setjjk
setjjk_POST = post_setjjk
setjjk_DEPS_CLEAN = clean_pre_setjjk
setjjk_SRCS = a.c 
setjjk_SRCS += jjk.c
setjjk_SRCS += k.cpp
setjjk_SRCS += ia.S ib.S
setjjk_SRCS += f.link.c
f_link_c_SRC = f.c
setjjk_SRCS += ic.link.S ibb.link.S
ic_link_S_SRC = ic.S
ibb_link_S_SRC = ibb.S
setjjk_SRCS += j.link.cpp
j_link_cpp_SRC = j.cpp
INCLUDE_FLAGS = -I${TOPDIR}/inc
setjjk_CFLAGS = -Wall -DCFILE=1 ${INCLUDE_FLAGS}
#setjjk_CPPFLAGS = -Wall -DCPPFILE=1 ${INCLUDE_FLAGS}
setjjk_LDFLAGS = -Wall -DLDFLILE=1 ${INCLUDE_FLAGS}
#setjjk_ASFLAGS = -Wall -DASFILE=1 ${INCLUDE_FLAGS}
d_link_c_SRC = d.c
f_link_cpp_SRC = g.cpp

main_SRCS = main.c b.c c.c
main_CFLAGS = -Wall -DMAIN_CFILE=1 ${INCLUDE_FLAGS}
main_CPPFLAGS = -Wall -DMAIN_CPPFILE=1 ${INCLUDE_FLAGS}
main_LDFLAGS = -Wall -DMAIN_LDFLILE=1 ${INCLUDE_FLAGS}
main_ASFLAGS = -Wall -DMAIN_ASFILE=1 ${INCLUDE_FLAGS}

#setjjk_LD = ${TOPDIR}/gpp.sh
#setjjk_GCC = ${TOPDIR}/gcc.sh
#setjjk_GPP = ${TOPDIR}/gpp.sh
#setjjk_GAS = ${TOPDIR}/gas.sh

all:post_setjjk main
#$(call call_all_exe,setjjk main)

post_setjjk: setjjk
	$(call call_exec,${TRUE},"POST","setjjk")

pre_setjjk:
	$(call call_exec,${TRUE},"PRE","setjjk")

clean_pre_setjjk:
	$(call call_exec,${TRUE},"CLEANPRE","setjjk")

clean_post_setjjk:clean_setjjk
	$(call call_exec,${TRUE},"CLEANPOST","setjjk")	

$(eval $(call simple_makefile_exe_whole,setjjk main))
#$(call foreach_makefile_exe_whole,setjjk main)

clean:clean_post_setjjk clean_main
#$(call call_clean_exe,setjjk main)
