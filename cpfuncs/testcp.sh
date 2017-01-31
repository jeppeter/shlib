#! /bin/bash

ECHO=`which echo`

source extargsparse4sh

INFO_LEVEL=2
DEBUG_LEVEL=3
WARN_LEVEL=1
ERROR_LEVEL=0

function __Debug()
{
        local _fmt=$1
        local _osname=`uname -s | tr [:upper:] [:lower:]`
        shift
        local _backstack=0
        if [ $# -gt 0 ]
                then
                _backstack=$1
        fi
        
        _fmtstr=""
        if [ $verbose -gt $INFO_LEVEL ]
                then
                if [ "$_osname" = "darwin" ]
                        then
                        local _filestack=`expr $_backstack \+ 1`
                        _fmtstr="${BASH_SOURCE[$_filestack]}:${BASH_LINENO[$_backstack]} "
                else
                        _fmtstr="${BASH_SOURCE[$_backstack]}:${BASH_LINENO[$_backstack]} "
                fi
        fi

        _fmtstr="$_fmtstr$_fmt"
        if [ "$_osname" = "darwin" ]
        	then
        	${ECHO} "$_fmtstr" >&2
        else
        	${ECHO} -e "$_fmtstr" >&2
    	fi
}

function Debug()
{
        local _fmt=$1
        shift
        local _backstack=0
        if [ $# -gt 0 ]
                then
                _backstack=$1
        fi
        _backstack=`expr $_backstack \+ 1`
        
        if [ $verbose -ge $DEBUG_LEVEL ]
                then
                __Debug "$_fmt" "$_backstack"
        fi
        return
}


function testcase_cpin_func()
{
	return
}

function get_testcase_funcnames()
{
	declare -f  | perl -ne 'if ($_ =~ m/^(testcase_[\w]+)\s+.*/o){print "$1\n";}'
	return
}

function clear_exit()
{
	if [ -n "$cpfromdir" ] && [ $reserved -eq 0 ]
		then
		if [ -d "$cpfromdir" ]
			then
			rm -rf "$cpfromdir"
		fi
	fi

	if [ -n "cptodir" ] && [ $reserved -eq 0 ]
		then
		if [ -d "$cptodir" ]
			then
			rm -rf "$cptodir"
		fi
	fi
}

funcstr="["
i=0
for curfunc in $(get_testcase_funcnames)
do
	if [ $i -gt 0 ]
		then
		funcstr="${funcstr},"
	fi
	funcstr="${funcstr}${curfunc}"
	i=`expr $i \+ 1`
done


read -r -d '' OPTIONS<<EOFMM
	{
		"verbose|v" : "+",
		"cpfromdir" : null,
		"cptodir" : null,
		"reserved|R" : false,
		"$<testfuncs>##can be on of($funcstr)##" : "*"
	}
EOFMM

parse_command_line "$OPTIONS" "$@"

if [ -n "$cpfromdir"  ]
	then
	export CP_SMB_DIR="$cpfromdir"
else
	
else

fi

if [ ${#testfuncs[@]} -gt 0 ]
	then
	for curfunc in "${testfuncs[@]}"
	do
		Debug "call [$curfunc]"
		eval "$curfunc"
	done
else
	for curfunc in $(get_testcase_funcnames)
	do
		Debug "call [$curfunc]"
		eval "$curfunc"
	done
fi