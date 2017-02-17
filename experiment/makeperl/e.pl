#! /usr/bin/env perl

###########################
## #! /usr/bin/env perl
## 
## use strict;
## my ($cmd) = "hello\"'\$\`\#";
## 
## print $cmd;
###########################

use strict;
my ($cmd) = "\#! /usr/bin/env perl\n\nuse strict;\nmy (\$cmd) = \"hello\\\"'\\\$\\\`\\\#\";\n\nprint \$cmd;";
eval $cmd;