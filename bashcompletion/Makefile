
TOPDIR=../

include ${TOPDIR}/basedef.mak

TOPDIR=$(call readlink_f,../)
CURDIR=$(call readlink_f,./)

ifeq (${P},)
PYTHON_CALL:=$(shell which python)
else
PYTHON_CALL:=${P}
endif

all:bashcomplete_format.py bashcomplete_test.py
	$(call call_exec,${PYTHON_CALL} ${CURDIR}/bashcomplete_test.py -v -f --releasemode,"TEST","bashcomplete_format.py")

bashcomplete_format.py:bashcomplete_format_debug.py bashcomplete_format.py.tmpl
	$(call call_exec,${PYTHON_CALL} bashcomplete_format_debug.py --basefile ${CURDIR}/bashcomplete.py.tmpl release;\
		_testcnt=0 ; _succ=0 ; \
		while [ $${_testcnt} -lt 10 ];\
		do \
		  if [ -f ${CURDIR}/bashcomplete_format.py.touched ]; \
		   then \
		   _succ=1 ;\
		   break ;\
		  fi ; \
		  ${PYTHON_CALL} -c "import time;time.sleep(0.5);" ;\
		  _testcnt=`expr $${_testcnt} \+ 1`;\
		 done; \
		 if [ $${_succ} -ne 1 ];\
		 then \
		 	${ECHO} "can not make bashcomplete_format.py" ;\
		 fi,"RELEASE","bashcomplete_format.py")
	$(call call_exec,${PYTHON_CALL} bashcomplete_format.py verify | ${DIFF} - ${CURDIR}/bashcomplete.py.tmpl,"VERIFY","bashcomplete_format.py")

clean:
	$(call call_exec,${RM} -f bashcomplete_format.py.touched,"RM","bashcomplete_format.py.touched")
	$(call call_exec,${RM} -f bashcomplete_format.py,"RM","bashcomplete_format.py")
