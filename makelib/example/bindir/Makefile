include ../../makelib.mak

TOPDIR:=$(call readlink_f,.)

osname:=$(call get_osname)

ifneq ($(patsubst cygwin_%,%,${osname}),${osname})
exesuffix:=.exe
else
exesuffix:=
endif


main_SRCS:= a.c main.c c.link.c
main_BINDIR:=${TOPDIR}/bin

c_link_c_SRC:= cl.c
main_CFLAGS := -Wall -I${TOPDIR}/inc
main_GCC:=${GCC}
main_LD:=${GCC}
CFLAGS += -I${TOPDIR}/inc
main_LDFLAGS:= -Wall
MAKEDEPS += ${TOPDIR}/Makefile

all:main${exesuffix}

$(eval $(call simple_makefile_exe_whole,main${exesuffix}))

clean:clean_main