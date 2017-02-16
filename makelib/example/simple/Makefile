
include ../../makelib.mak

TOPDIR:=$(call readlink_f,.)

jjk_SRCS = jjk.c
jjk_SRCS += a.c 
jjk_SRCS += k.cpp
jjk_SRCS += ia.S ib.S
jjk_SRCS += f.link.c
f_link_c_SRC = f.c
jjk_SRCS += ic.link.S ibb.link.S
ic_link_S_SRC = ic.S
ibb_link_S_SRC = ibb.S
jjk_SRCS += j.link.cpp
j_link_cpp_SRC = j.cpp
INCLUDE_FLAGS = -I${TOPDIR}/inc
jjk_CFLAGS = -Wall -DCFILE=1 ${INCLUDE_FLAGS}
#jjk_CPPFLAGS = -Wall -DCPPFILE=1 ${INCLUDE_FLAGS}
jjk_LDFLAGS = -Wall -DLDFLILE=1 ${INCLUDE_FLAGS}
#jjk_ASFLAGS = -Wall -DASFILE=1 ${INCLUDE_FLAGS}
d_link_c_SRC = d.c
f_link_cpp_SRC = g.cpp

main_SRCS = main.c b.c c.c
main_CFLAGS = -Wall -DMAIN_CFILE=1 ${INCLUDE_FLAGS}
main_CPPFLAGS = -Wall -DMAIN_CPPFILE=1 ${INCLUDE_FLAGS}
main_LDFLAGS = -Wall -DMAIN_LDFLILE=1 ${INCLUDE_FLAGS}
main_ASFLAGS = -Wall -DMAIN_ASFILE=1 ${INCLUDE_FLAGS}

#jjk_LD = ${TOPDIR}/gpp.sh
#jjk_GCC = ${TOPDIR}/gcc.sh
#jjk_GPP = ${TOPDIR}/gpp.sh
#jjk_GAS = ${TOPDIR}/gas.sh

all:jjk main

$(call simple_makefile_exe_whole,jjk main)

clean:$(patsubst %,clean_%,jjk main)