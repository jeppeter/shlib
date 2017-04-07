#! /bin/bash



if [ -z "$PYTHON" ]
	then
	PYTHON=python
fi

rm -f complete.py
$PYTHON bashcomplete_format_debug.py -o complete.py --prefix bashcomplete_format --basefile bashcomplete.py.tmpl --jsonfile test.json debug
$PYTHON complete.py --line 'insertcode ~' --index 12 --jsonfile test.json -vvvvv complete -- insertcode '~'