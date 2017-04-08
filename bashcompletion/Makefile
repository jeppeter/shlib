
TOPDIR=../
ifeq (${V},)
Q=@
else
Q=
endif

include ${TOPDIR}/basedef.mak

TOPDIR=$(call readlink_f,../)
CURDIR=$(call readlink_f,./)

ifeq (${P},)
PYTHON_CALL:=$(shell which python)
else
PYTHON_CALL:=${P}
endif

all:bashcomplete_format.completion


bashcomplete_format.completion : bashcomplete_format bashcomplete_test.py
	$(call call_exec,${PYTHON_CALL} ${CURDIR}/bashcomplete_test.py -v -f --releasemode,"TEST","bashcomplete_format")
	$(call call_exec,${PYTHON_CALL} ${CURDIR}/bashcomplete_format -o $@ selfcomp,"MAKE","bashcomplete_format.completion")

bashcomplete_format:bashcomplete_format_debug.py bashcomplete_format.py.tmpl
	$(call call_exec,${PYTHON_CALL} bashcomplete_format_debug.py --basefile ${CURDIR}/bashcomplete.py.tmpl --output $@ release;\
		_testcnt=0 ; _succ=0 ; \
		while [ $${_testcnt} -lt 10 ];\
		do \
		  if [ -f ${CURDIR}/bashcomplete_format.touched ]; \
		   then \
		   _succ=1 ;\
		   break ;\
		  fi ; \
		  ${PYTHON_CALL} -c "import time;time.sleep(0.5);" ;\
		  _testcnt=`expr $${_testcnt} \+ 1`;\
		 done; \
		 if [ $${_succ} -ne 1 ];\
		 then \
		 	${ECHO} "can not make bashcomplete_format" ;\
		 fi,"RELEASE","bashcomplete_format")
	$(call call_exec,${PYTHON_CALL} $@ verify | ${DIFF} - ${CURDIR}/bashcomplete.py.tmpl,"VERIFY","bashcomplete_format")
	$(call call_exec,chmod +x $@,"CHX","bashcomplete_format")

clean:
	$(call call_exec,${RM} -f bashcomplete_format.touched,"RM","bashcomplete_format.touched")
	$(call call_exec,${RM} -f bashcomplete_format,"RM","bashcomplete_format")
	$(call call_exec,${RM} -f bashcomplete_format.completion,"RM","bashcomplete_format.completion")
