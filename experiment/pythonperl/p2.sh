#! /bin/sh

ECHO_STR="use strict;my (\$cmd)=\"\#! /usr/bin/env perl\n\nuse strict;\nmy (\\\$cmd)=\\\"\\\\\\\"'\\\\\\\\\\\\\@\\\\\\\$\\\\&\\\\\`\\\";\nprint \\\$cmd;\";print \$cmd;"
perl -e "${ECHO_STR}"