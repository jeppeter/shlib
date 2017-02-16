
include ../../makelib.mak

TOPDIR:=$(call readlink_f,.)

main_SRCS = c.c a.c b.c  main.c
#main_SRCS += main.cpp
#main_SRCS += ia.S ib.S
#main_SRCS += ic.link.S ibb.link.S
#main_SRCS += j.link.cpp f.link.c
#ic_link_S_SRC = ic.S
#ibb_link_S_SRC = ibb.S
#j_link_cpp_SRC = j.cpp
#f_link_c_SRC = f.c
INCLUDE_FLAGS = -I${TOPDIR}/inc
main_CFLAGS = -Wall -DCFILE=1 ${INCLUDE_FLAGS}
main_CPPFLAGS = -Wall -DCPPFILE=1 ${INCLUDE_FLAGS}
main_LDFLAGS = -Wall -DLDFLILE=1 ${INCLUDE_FLAGS}
main_ASFLAGS = -Wall -DASFILE=1 ${INCLUDE_FLAGS}
main_COMPILER = gcc
d_link_c_SRC = d.c
f_link_cpp_SRC = g.cpp
main_LD = gcc
main_GCC = gcc

define ld_run_direct
$(call call_exec,$(5) $(3) -o $(1) $(2) $(4),"LD","$(call get_basename,$(1))")
endef

define build_exe_only
$(1) : $(2)
	$(call ld_run_direct,$(1),$(2),$(3),$(4),$(5))
endef

define call_include_function
$(info "function include[$(1)]")
-include $(1)
endef

define build_objs_c
$(info "cobj[$(1)] csrc[$(2)] shortname[$(3)]  deps[$(4)] cflags[$(5)] compiler[$(6)]")
-include $(4)
$(1) : $(2) $(4) $$(MAKEDEPS) $$($(3)_DEPS)
	$${Q}$(call build_c,$(1),$(2),$(3),$(5),$(6))

$(4) : $$($(3)_DEPS)
	$${Q}$(call build_c_depends,$(2),$(4),$(3),$(5),$(6))
endef

define build_objs_cpp
$(info "cppobj[$(1)] cppsrc[$(2)] shortname[$(3)]  deps[$(4)] cppflags[$(5)] compiler[$(6)]")
-include $(4)
$(1) : $(2) $$(MAKEDEPS) $$($(3)_DEPS)
	$${Q}$(call build_cpp,$(1),$(2),$(3),$(5),$(6))

$(4) :  $$($(3)_DEPS)
	$${Q}$(call build_cpp_depends,$(2),$(4),$(3),$(5),$(6))
endef

define build_objs_S
$(info "Sobj[$(1)] Ssrc[$(2)] shortname[$(3)]  deps[$(4)] sflags[$(5)] compiler[$(6)]")
$(1) : $(2) $(4) $$(MAKEDEPS) $$($(3)_DEPS)
	$${Q}$(call build_S,$(1),$(2),$(3),$(5),$(6))

$(4) : $$($(3)_DEPS)
	$${Q}$(call build_S_depends,$(2),$(4),$(3),$(5),$(6))
endef

define build_objs_link_c
$(info "cobj[$(1)] csrc[$(2)] shortname[$(3)]  deps[$(4)] cflags[$(5)] compiler[$(6)]")
-include $(4)
$(1) : $(2) $(4) $$(MAKEDEPS) $$($(3)_DEPS)
	$${Q}$(call build_c,$(1),$(2),$(3),$(5),$(6))

$(4) : $$($(3)_DEPS) $$($(3)_SRC)
	$${Q}$$(call link_c_file,$$($(3)_SRC),$(2))
	$${Q}$$(call build_c_depends,$(2),$(4),$(3),$(5),$(6))
endef

define build_objs_link_cpp
$(info "cppobj[$(1)] cppsrc[$(2)] shortname[$(3)]  deps[$(4)] cppflags[$(5)] compiler[$(6)]")
-include $(4)
$(1) : $(2) $(4) $$(MAKEDEPS) $$($(3)_DEPS)
	$${Q}$(call build_cpp,$(1),$(2),$(3),$(5),$(6))

$(4) : $$($(3)_DEPS) $$($(3)_SRC)
	$${Q}$$(call link_cpp_file,$$($(3)_SRC),$(2))
	$${Q}$$(call build_cpp_depends,$(2),$(4),$(3),$(5),$(6))
endef

define build_objs_link_S
$(info "Sobj[$(1)] Ssrc[$(2)] shortname[$(3)]  deps[$(4)] asflags[$(5)] compiler[$(6)]")
-include $(4)
$(1) : $(2) $(4) $$(MAKEDEPS) $$($(3)_DEPS)
	$${Q}$(call build_S,$(1),$(2),$(3),$(5),$(6))

$(4) : $$($(3)_DEPS) $$($(3)_SRC)
	$${Q}$$(call link_S_file,$$($(3)_SRC),$(2))
	$${Q}$$(call build_S_depends,$(2),$(4),$(3),$(5),$(6))
endef

define build_clean_exe_only
$(call call_exec,${RM} -f $(1),"RM","$(call get_basename,$(1))")
endef



#####################################
##  input $(1)  src files
##        $(2)  shortname
##        $(3)  flags
##        $(4)  compiler
#####################################
define foreach_build_objs_c
$(foreach cursrc,$(1),\
$(eval $(call build_objs_c,$(call get_toobj,$(cursrc),\
${PWD},$($(2)_BINDIR)),$(cursrc),$(call get_shortname,$(cursrc),$($(2)_BASEDIR)),$(call get_depname,$(cursrc),${PWD},$($(2)_BINDIR)),$(3),$(4))))
endef


define foreach_include
$(foreach cursrc,main.c a.c b.c c.c,$(eval $(call call_include_function,$(call get_depname,$(cursrc)))))
endef


$(eval $(call build_exe_only,main,$(call get_toobj,$(main_SRCS)),$(main_LDFLAGS),$(main_LIBFLAGS),$(main_LD)))
$(call foreach_c_file_shortname,$(call get_cfile,$(main_SRCS)),${PWD},$(main_CFLAGS),${GCC})



clean:
	$(call call_exec,${RM} -f $(call get_toobj,$(main_SRCS)) ,"RM","main_objs")
	$(call call_exec,${RM} -f main,"RM","main")