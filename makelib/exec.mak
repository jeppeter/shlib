
ifndef __EXEC_MAK__
define __EXEC_MAK__

define call_exec_echo
${PRINTF} "    %-9s %s\n" $(1) $(2);
endef

ifeq (${Q},)
define call_exec_directly
$(1)
endef
else
define call_exec_directly
$(call call_exec_echo,$(2),$(3)) $(1)
endef
endif

define call_exec
${Q}$(call call_exec_directly,$(1),$(2),$(3))
endef


## __EXEC_MAK__ ##
endif