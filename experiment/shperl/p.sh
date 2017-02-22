#! /bin/sh


############################
## #! /usr/bin/env perl
## 
## my ($cmd)="hello\"'\$\$\@\\";
## print $cmd;
############################

ECHO_STR="#! /usr/bin/env perl\n\nmy (\$cmd)=\"hello\\\"'\\\$\\\$\\\@\\\\\";\nprint \$cmd;"
perl -e "use strict;my (\$cmd)=\"\#! /usr/bin/env perl\n\nmy (\\\$cmd)=\\\"hello\\\\\`\\\\\\\"'\\\\\\\$\\\\\\\$\\\\\@\\\\\\\\\\\";\nprint \\\$cmd;\";print \$cmd;"