#! /bin/sh

################################
## #! /usr/bin/env python
## 
## cmd='hello`"\'$$@\\'
## print('%s'%(cmd))
################################
python -c "import sys;cmd='#! /usr/bin/env python\n\ncmd=\\'hello\`\"\\\\\\'\$\$@\\\\\\\\\\'\nprint(\\'%s\\'%(cmd))';sys.stdout.write('%s'%(cmd))"