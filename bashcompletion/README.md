# extargsparse 
> python command package for json string set

### Release History
* Apr 9th 2017 Release 0.1.2 to release first available use version

### howto use
> please make sure pip install extargsparse cmdpack disttools
> and run make all you will find bashcomplete_format file output


### example 
> simpleuse

```python
# !/usr/bin/env python
import sys
import os

_extargs_parent_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..'))
if _extargs_parent_dir not in sys.path:
    _temp_path = sys.path
    sys.path = [_extargs_parent_dir]
    sys.path.extend(_temp_path)
import extargsparse

commandline = '''
{
    "verbose|v##increment verbose mode##" : "+",
    "flag|f## flag set##" : false,
    "number|n" : 0,
    "list|l" : [],
    "string|s" : "string_var",
    "$" : "*"
}
'''

def main():
    parser = extargsparse.ExtArgsParse(usage=' sample commandline parser ')
    parser.load_command_line_string(commandline)
    args = parser.parse_command_line()
    print ('verbose = %d'%(args.verbose))
    print ('flag = %s'%(args.flag))
    print ('number = %d'%(args.number))
    print ('list = %s'%(args.list))
    print ('string = %s'%(args.string))
    print ('args = %s'%(args.args))

if __name__ == '__main__':
	main()
```

```json
{
    "verbose|v##increment verbose mode##" : "+",
    "flag|f## flag set##" : false,
    "number|n" : 0,
    "list|l" : [],
    "string|s" : "string_var",
    "$" : "*"
}
```

> run command

```shell
bashcomplete_format --prefix simpleuse --jsonfile simpleuse.json output --output simpleuse.completion
```

> the file simpleuse.completion is the file for 
> in bash mode call 
```shell
source simpleuse.completion
```

> when you type simpleuse it will give the completion notation for you