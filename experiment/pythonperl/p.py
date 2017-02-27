#! /usr/bin/env python

import sys
cmd='#! /usr/bin/env perl\n\nuse strict;\nmy ($cmd)=\"\\\"\'\\\\\@\\$\\&\\`\";\nprint $cmd;'
sys.stdout.write('%s'%(cmd))