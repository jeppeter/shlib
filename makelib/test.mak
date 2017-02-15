
include ./makelib.mak

main_SRCS= c.c a.c b.c main.cpp
main_CFLAGS = -Wall -DCFILE=1
main_CPPFLAGS = -Wall -DCPPFILE=1
main_LDFLAGS = -Wall -DLDFLILE=1
d_link_c_SRC = d.c
f_link_cpp_SRC = g.cpp

define build_exe_only
$(1) : $(2)
	$(call call_exec,${TRUE},"LD","$(1)")
	$(call call_exec,${TRUE},"OBJS","$(2)")
	$(call call_exec,${TRUE},"LDFLAGS","$(3)")
	$(call call_exec,${TRUE},"COMPILER","$(4)")
endef

define build_objs_c
$(1) : $(2)
	$(call call_exec,${TRUE},"CC","$(1)")
	$(call call_exec,${TRUE},"CFLAGS","$(3)")
	$(call call_exec,${TRUE},"COMPILER","$(4)")

$(2) :
	$(call call_exec,${TRUE},"CFILE","$(2)")
endef

define build_objs_cpp
$(info "1[$(1)] 2[$(2)] 3[$(3)] 4[$(4)]")
$(1) : $(2)
	$(call call_exec,${TRUE},"CPP","$(1)")
	$(call call_exec,${TRUE},"CPPFLAGS","$(3)")
	$(call call_exec,${TRUE},"COMPILER","$(4)")

$(2) :
	$(call call_exec,${TRUE},"ECHO","$(2)")
endef

define build_objs_S
$(1) : $(2)
	$(call call_exec,${TRUE},"ASM","$(1)")
	$(call call_exec,${TRUE},"ASMFLAGS","$(3)")
	$(call call_exec,${TRUE},"COMPILER","$(4)")

$(2) :
	$(call call_exec,${TRUE},"ECHO","$(2)")
endef

define build_objs_link_c
$(1) : $(2)
	$(call call_exec,${TRUE},"CC","$$@")
	$(call call_exec,${TRUE},"CFLAGS","$(3)")
	$(call call_exec,${TRUE},"COMPILER","$(4)")

$(2) : $$($(3)_SRC)
	$(call call_exec,${TRUE},"LINK","$$@")

$$($(3)_SRC) :
	$(call call_exec,${TRUE},"ECHO","$$@")
endef

define build_objs_link_cpp
$(1) : $(2)
	$(call call_exec,${TRUE},"CC","$$@")
	$(call call_exec,${TRUE},"CPPFLAGS","$(3)")
	$(call call_exec,${TRUE},"COMPILER","$(4)")

$(2) : $$($(3)_SRC)
	$(call call_exec,${TRUE},"LINK","$$@")

$$($(3)_SRC) :
	$(call call_exec,${TRUE},"ECHO","$$@")
endef

define build_objs_link_S
$(1) : $(2)
	$(call call_exec,${TRUE},"CC","$$@")
	$(call call_exec,${TRUE},"ASMFLAGS","$(3)")
	$(call call_exec,${TRUE},"COMPILER","$(4)")

$(2) : $$($(3)_SRC)
	$(call call_exec,${TRUE},"LINK","$$@")

$$($(3)_SRC) :
	$(call call_exec,${TRUE},"ECHO","$$@")
endef


#####################################
##  input $(1)  exe name
##        $(2)  src name
##        $(3)  shortname
##        $(4)  compilter
#####################################
define build_exe_objs
$(foreach cursrc,$(call \
	get_cfile,$(2)),\
$(eval 
	$(call 
		build_objs_c,$(call 
			get_toobj,$(cursrc)),$(cursrc),\
$(call \
	get_default_value,$($(call \
		get_exename,$(1))_CFLAGS),${CFLAGS}),$(call \
				get_default_value,\
$($(call 
	get_exename,$(1))_COMPILER,${GCC})\
)\
)\
)\
)
endef

define foreac_build_objs_c
$(foreach cursrc,$(1),\
$(eval $(call build_objs_c,$(call get_toobj,$(cursrc)),$(cursrc),$(2),$(3))))
endef

define foreac_build_objs_cpp
$(foreach cursrc,$(1),\
$(eval $(call build_objs_cpp,$(call get_toobj,$(cursrc)),$(cursrc),$(2),$(3))))
endef


# all:
# 	$(call call_exec,${TRUE},"GET","$(call get_toobj,hello.c hello.cpp hello.S main.link.cpp)")
# 	$(call call_exec,${TRUE},"CFILE","$(call get_cfile,hello.c hello.cpp hello.S main.link.cpp)")
# 	$(call call_exec,${TRUE},"CPPFILE","$(call get_cppfile,hello.c hello.cpp hello.S main.link.cpp)")
# 	$(call call_exec,${TRUE},"LCPPFILE","$(call get_lcppfile,hello.c hello.cpp hello.S main.link.cpp)")
# 	$(call call_exec,${TRUE},"LCFILE","$(call get_lcfile,hello.c hello.cpp hello.S main.link.cpp)")
# 	$(call call_exec,${TRUE},"SFILE","$(call get_sfile,hello.c hello.cpp hello.S main.link.cpp)")
# 	$(call call_exec,${TRUE},"LSFILE","$(call get_lsfile,hello.c hello.cpp hello.S main.link.cpp)")

$(call build_exe_only,main,$(call get_toobj,$(main_SRCS)),$(main_LDFLAGS),$(main_COMPILER))
$(call foreac_build_objs_c,$(call get_cfile,$(main_SRCS)),$(main_CFLAGS),$(main_COMPILER))
$(call foreac_build_objs_cpp,$(call get_cppfile,$(main_SRCS)),$(main_CPPFLAGS),$(main_COMPILER))
#$(foreach cursrc,$(call get_cfile,$(main_SRCS)),$(info "$(cursrc)"))

