
include ./makelib.mak

main_SRCS= c.c a.c b.c main.cpp d.link.c f.link.cpp
d_link_c_SRC = d.c
f_link_cpp_SRC = g.cpp

define build_exe_only
$(1) : $(2)
	$(call call_exec,${TRUE},"LD","$(1)")
	$(call call_exec,${TRUE},"CC","$(2)")
endef

define build_objs_c
$(1) : $(2)
	$(call call_exec,${TRUE},"CC","$(1)")

$(2) :
	$(call call_exec,${TRUE},"ECHO","$(2)")
endef

define build_objs_cc
$(1) : $(2)
	$(call call_exec,${TRUE},"CPP","$(1)")

$(2) :
	$(call call_exec,${TRUE},"ECHO","$(2)")
endef

define build_objs_S
$(1) : $(2)
	$(call call_exec,${TRUE},"ASM","$(1)")

$(2) :
	$(call call_exec,${TRUE},"ECHO","$(2)")
endef

define build_objs_link_c
$(1) : $(2)
	$(call call_exec,${TRUE},"CC","$$@")

$(2) : $$($(3)_SRC)
	$(call call_exec,${TRUE},"LINK","$$@")

$$($(3)_SRC) :
	$(call call_exec,${TRUE},"ECHO","$$@")
endef

define build_objs_link_cpp
$(1) : $(2)
	$(call call_exec,${TRUE},"CC","$$@")

$(2) : $$($(3)_SRC)
	$(call call_exec,${TRUE},"LINK","$$@")

$$($(3)_SRC) :
	$(call call_exec,${TRUE},"ECHO","$$@")
endef


define build_exe_objs
$(foreach cursrc,$(call get_cfile,$(2)),\
$(eval $(call build_objs_c,$(call get_toobj,$(cursrc)),$(cursrc),\
$(call get_))))
endef


$(eval $(call build_exe_only,main,$(main_SRCS)))