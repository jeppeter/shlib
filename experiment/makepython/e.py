#! /usr/bin/env python

#############################
## #! /usr/bin/env python
## 
## import sys
## cmd = 'hello"\'$$`@_#%'
## sys.stdout.write('%s'%(cmd))
#############################

import sys
cmd='#! /usr/bin/env python\n\nimport sys\ncmd = \'hello"\\\'$$`@_#%\'\nsys.stdout.write(\'%s\'%(cmd))'
exec('%s'%(cmd))