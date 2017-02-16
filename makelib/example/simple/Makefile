
include ../../makelib.mak

main_SRCS = c.c a.c b.c  main.c
#main_SRCS += main.cpp
#main_SRCS += ia.S ib.S
#main_SRCS += ic.link.S ibb.link.S
#main_SRCS += j.link.cpp f.link.c
#ic_link_S_SRC = ic.S
#ibb_link_S_SRC = ibb.S
#j_link_cpp_SRC = j.cpp
#f_link_c_SRC = f.c
main_CFLAGS = -Wall -DCFILE=1 
main_CPPFLAGS = -Wall -DCPPFILE=1
main_LDFLAGS = -Wall -DLDFLILE=1
main_COMPILER = gcc
d_link_c_SRC = d.c
f_link_cpp_SRC = g.cpp


define ld_run_direct
$(call call_exec,$(call get_default_value,$(5),${GPP}) $(3) -o $(2) $(1) $(4),"LD","$(call get_basename,$(1))")
endef

define build_exe_only
$(info "exeonly  dest[$(1)] objs[$(2)] ldflags[$(3)] libflags[$(4)] compiler[$(5)]")
$(1) : $(2)
	$(call ld_run_direct,$(1),$(2),$(3),$(4),$(5))
endef

define build_objs_c
$(info "cobj[$(1)] csrc[$(2)] shortname[$(3)]  deps[$(4)] cflags[$(5)] compiler[$(6)]")
-include $(4)
$(1) : $(2) $(4) $$(MAKEDEPS) $$($(3)_DEPS)
	$${Q}$(call build_c,$(1),$(2),$(3),$(5),$(6))

$(4) : $(2) $$($(3)_DEPS)
	$${Q}$(call build_c_depends,$(2),$(4),$(3),$(5),$(6))
endef

define build_objs_cpp
$(info "cppobj[$(1)] cppsrc[$(2)] shortname[$(3)]  deps[$(4)] cppflags[$(5)] compiler[$(6)]")
-include $(4)
$(1) : $(2) $$(MAKEDEPS) $$($(3)_DEPS)
	$${Q}$(call build_cpp,$(1),$(2),$(3),$(5),$(6))

$(4) : $(2) $$($(3)_DEPS)
	$${Q}$(call build_cpp_depends,$(2),$(4),$(3),$(5),$(6))
endef

define build_objs_S
$(info "Sobj[$(1)] Ssrc[$(2)] shortname[$(3)]  deps[$(4)] sflags[$(5)] compiler[$(6)]")
$(1) : $(2) $(4) $$(MAKEDEPS) $$($(3)_DEPS)
	$${Q}$(call build_S,$(1),$(2),$(3),$(5),$(6))

$(4) : $(2) $$($(3)_DEPS)
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



#####################################
##  input $(1)  src files
##        $(2)  shortname
##        $(3)  flags
##        $(4)  compiler
#####################################
define foreach_build_objs_c
$(foreach cursrc,$(1),$(eval $(call build_objs_c,$(call get_toobj,$(cursrc),${PWD},$($(2)_BINDIR)),$(cursrc),$(call get_shortname,$(cursrc),$($(2)_BASEDIR)),$(call ),$(3),$(4))))
endef



$(eval $(call build_exe_only,main,$(call get_toobj,$(main_SRCS)),$(main_LDFLAGS),$(main_LIBFLAGS),$(main_LD)))
$(foreach_build_objs_c,$(call get_cfile,$(main_SRCS)),main,$(main_CFLAGS),$(main_GCC))

