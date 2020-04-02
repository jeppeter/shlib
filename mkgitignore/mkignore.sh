#! /bin/bash

function mk_ignore()
{
	local _rootdir=$1

	for _c in $(find "$_rootdir" -type d)
	do
		touch "$_c/.gitignore"
	done
}

while [ $# -gt 0 ]
do
	mk_ignore "$1"
	shift
done