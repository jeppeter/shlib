include ../../makelib.mak

osname=$(call get_osname)
sharesuffix=
ifeq (${osname},darwin)
sharesuffix=dylib
endif

ifeq (${osname},linux)
sharesuffix=so
endif

ifneq ($(patsubst cygwin_%,%,${osname}),${osname})
sharesuffix=dll
endif

ifeq (${sharesuffix},)
$(error "platform ${osname} not supported")
endif

libshare_${sharesuffix}_SRCS = sc.c sd.cpp
libshare_${sharesuffix}_SRCS += se.link.cpp sf.link.c
libshare_${sharesuffix}_SRCS += sg.S sh.link.S

se_link_cpp_SRC = si.cpp
sf_link_c_SRC = sj.c
sh_link_S_SRC = sk.S

CURDIR:= $(call readlink_f,.)

INCLUDES = -I${CURDIR}/incs

COMMA=,
ifeq (${osname},linux)
libshare_${sharesuffix}_CFLAGS = -Wall -fpic -DCFILE=1 ${INCLUDES}  -I${CURDIR}/cinc
libshare_${sharesuffix}_CPPFLAGS = -Wall -fpic -DCPPFILE=1 ${INCLUDES} -I${CURDIR}/cppinc
libshare_${sharesuffix}_ASFLAGS = -Wall -fpic -DASFILE=1 ${INCLUDES} -I${CURDIR}/sinc
libshare_${sharesuffix}_LDFLAGS = -Wall -shared -Wl${COMMA}-soname${COMMA}libshare.so.1
endif

ifeq (${osname},darwin)
libshare_${sharesuffix}_CFLAGS = -Wall  -DCFILE=1 ${INCLUDES}  -I${CURDIR}/cinc
libshare_${sharesuffix}_CPPFLAGS = -Wall  -DCPPFILE=1 ${INCLUDES} -I${CURDIR}/cppinc
libshare_${sharesuffix}_ASFLAGS = -Wall  -DASFILE=1 ${INCLUDES} -I${CURDIR}/sinc
libshare_${sharesuffix}_LDFLAGS = -Wall -dynamiclib -compatibility_version 1.2 -current_version 1.2.6 -undefined suppress -flat_namespace
endif

ifneq ($(patsubst cygwin_%,%,${osname}),${osname})
libshare_${sharesuffix}_CFLAGS = -Wall -fpic -DCFILE=1 ${INCLUDES}  -I${CURDIR}/cinc
libshare_${sharesuffix}_CPPFLAGS = -Wall -fpic -DCPPFILE=1 ${INCLUDES} -I${CURDIR}/cppinc
libshare_${sharesuffix}_ASFLAGS = -Wall -fpic -DASFILE=1 ${INCLUDES} -I${CURDIR}/sinc
libshare_${sharesuffix}_LDFLAGS = -Wall -shared 
endif

libdyn_${sharesuffix}_SRCS = dc.c dd.cpp
libdyn_${sharesuffix}_SRCS += de.link.cpp df.link.c
libdyn_${sharesuffix}_SRCS += dg.S dh.link.S

de_link_cpp_SRC = di.cpp
df_link_c_SRC = dj.c
dh_link_S_SRC = dk.S

ifeq (${osname},linux)
libdyn_${sharesuffix}_CFLAGS = -Wall -fpic -DCFILE=1 ${INCLUDES}  -I${CURDIR}/cinc
libdyn_${sharesuffix}_CPPFLAGS = -Wall -fpic -DCPPFILE=1 ${INCLUDES} -I${CURDIR}/cppinc
libdyn_${sharesuffix}_ASFLAGS = -Wall -fpic -DASFILE=1 ${INCLUDES} -I${CURDIR}/sinc
libdyn_${sharesuffix}_LDFLAGS = -Wall -shared -Wl${COMMA}-soname${COMMA}libdyn.so.1
endif

ifeq (${osname},darwin)
libdyn_${sharesuffix}_CFLAGS = -Wall -DCFILE=1 ${INCLUDES}  -I${CURDIR}/cinc
libdyn_${sharesuffix}_CPPFLAGS = -Wall -DCPPFILE=1 ${INCLUDES} -I${CURDIR}/cppinc
libdyn_${sharesuffix}_ASFLAGS = -Wall -DASFILE=1 ${INCLUDES} -I${CURDIR}/sinc
libdyn_${sharesuffix}_LDFLAGS = -Wall -dynamiclib -compatibility_version 1.2 -current_version 1.2.6 -undefined suppress -flat_namespace
endif

ifneq ($(patsubst cygwin_%,%,${osname}),${osname})
libdyn_${sharesuffix}_CFLAGS = -Wall -fpic -DCFILE=1 ${INCLUDES}  -I${CURDIR}/cinc
libdyn_${sharesuffix}_CPPFLAGS = -Wall -fpic -DCPPFILE=1 ${INCLUDES} -I${CURDIR}/cppinc
libdyn_${sharesuffix}_ASFLAGS = -Wall -fpic -DASFILE=1 ${INCLUDES} -I${CURDIR}/sinc
libdyn_${sharesuffix}_LDFLAGS = -Wall -shared
endif


all:libshare.${sharesuffix} libdyn.${sharesuffix}


#$(eval $(call makefile_so_whole,libshare.so.1.2.3))
$(call simple_makefile_so_whole,libshare.${sharesuffix} libdyn.${sharesuffix})

#$(call make_so_whole,libshare.so.1.2.3)
#$(call clean_so_whole,libshare.so.1.2.3)

clean:clean_libshare_${sharesuffix} clean_libdyn_${sharesuffix}
