
PRINTF:=$(shell which printf)

define call_exec_echo
${PRINTF} "    %-9s %s\n" $(1) $(2);
endef

define call_run_command
$(1)
endef

ifeq (${Q},)
define call_exec_directly
$(call call_run_command,$(1))
endef
else
define call_exec_directly
$(call call_exec_echo,$(2),$(3)) $(call call_run_command,$(1))
endef
endif

define call_exec
${Q}$(call call_exec_directly,$(1),$(2),$(3))
endef
