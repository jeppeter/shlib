#! /usr/bin/env python

import sys
cmd='#! /bin/sh\n\nECHO_STR="use strict;my (\\$cmd)=\\"\\#! /usr/bin/env perl\\n\\nuse strict;\\nmy (\\\\\\$cmd)=\\\\\\"\\\\\\\\\\\\\\"\'\\\\\\\\\\\\\\\\\\\\\\\\\\@\\\\\\\\\\\\\\$\\\\\\\\&\\\\\\\\\\`\\\\\\";\\nprint \\\\\\$cmd;\\";print \\$cmd;"\nperl -e "${ECHO_STR}"'
sys.stdout.write('%s'%(cmd))