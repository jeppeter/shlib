#! /bin/bash



if [ -z "$PYTHON" ]
	then
	PYTHON=python
fi

rm -f complete.py
$PYTHON bashcomplete_format_debug.py -o complete.py --prefix bashcomplete_format --basefile bashcomplete.py.tmpl --jsonfile test.json debug
$PYTHON complete.py --line "bashcomplete_format -o 'space " --index 30 --jsonfile test.json -vvvvv complete -- bashcomplete_format -o 'space '