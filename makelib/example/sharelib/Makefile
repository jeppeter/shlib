include ../../makelib.mak

libshare_so_SRCS = sc.c sd.cpp
libshare_so_SRCS += se.link.cpp sf.link.c
libshare_so_SRCS += sg.S sh.link.S

se_link_cpp_SRC = si.cpp
sf_link_c_SRC = sj.c
sh_link_S_SRC = sk.S

CURDIR:= $(call readlink_f,.)

INCLUDES = -I${CURDIR}/incs

COMMA=,
libshare_so_CFLAGS = -Wall -fpic -DCFILE=1 ${INCLUDES}  -I${CURDIR}/cinc
libshare_so_CPPFLAGS = -Wall -fpic -DCPPFILE=1 ${INCLUDES} -I${CURDIR}/cppinc
libshare_so_ASFLAGS = -Wall -fpic -DASFILE=1 ${INCLUDES} -I${CURDIR}/sinc
libshare_so_LDFLAGS = -Wall -shared -Wl${COMMA}-soname${COMMA}libshare.so.1

all:libshare.so.1.2.3

$(call make_so_whole,libshare.so.1.2.3)
$(call clean_so_whole,libshare.so.1.2.3)

clean:clean_libshare_so
