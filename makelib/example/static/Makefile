include ../../makelib.mak

libstatic_a_SRCS = sc.c sd.cpp
libstatic_a_SRCS += se.link.cpp sf.link.c
libstatic_a_SRCS += sg.S sh.link.S

se_link_cpp_SRC = si.cpp
sf_link_c_SRC = sj.c
sh_link_S_SRC = sk.S

CURDIR:= $(call readlink_f,.)

INCLUDES = -I${CURDIR}/incs

libstatic_a_CFLAGS = -Wall  -DCFILE=1 ${INCLUDES}  -I${CURDIR}/cinc
libstatic_a_CPPFLAGS = -Wall  -DCPPFILE=1 ${INCLUDES} -I${CURDIR}/cppinc
libstatic_a_ASFLAGS = -Wall  -DASFILE=1 ${INCLUDES} -I${CURDIR}/sinc
libstatic_a_ARFLAGS = 
libstatic_a_AR = ${AR}

libnodyn_a_SRCS = dc.c dd.cpp
libnodyn_a_SRCS += de.link.cpp df.link.c
libnodyn_a_SRCS += dg.S dh.link.S

de_link_cpp_SRC = di.cpp
df_link_c_SRC = dj.c
dh_link_S_SRC = dk.S

libnodyn_a_CFLAGS = -Wall  -DCFILE=1 ${INCLUDES}  -I${CURDIR}/cinc
libnodyn_a_CPPFLAGS = -Wall  -DCPPFILE=1 ${INCLUDES} -I${CURDIR}/cppinc
libnodyn_a_ASFLAGS = -Wall  -DASFILE=1 ${INCLUDES} -I${CURDIR}/sinc
libnodyn_a_ARFLAGS = 
libnodyn_a_AR = ${AR}

all:libstatic.a libnodyn.a

#$(eval $(call clean_staticlib_whole,libstatic.a))
#$(eval $(call make_staticlib_whole,libstatic.a))
#$(eval $(call makefile_staticlib_whole,libstatic.a))
#$(call foreach_makefile_staticlib_whole,libstatic.a)
$(call simple_makefile_staticlib_whole,libstatic.a libnodyn.a)

clean:clean_libstatic_a clean_libnodyn_a
