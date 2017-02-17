# makelib.mak
> GNU Makefile library


### Release History
* Feb 16th 2017 Release 0.1.0 for first usable version

### simple example
> directory structure
```shell
.
├── a.c
├── b.c
├── c.c
├── f.c
├── gas.sh
├── gcc.sh
├── gpp.sh
├── ia.S
├── ibb.S
├── ib.S
├── ic.S
├── inc
│   ├── a.h
│   ├── b.h
│   ├── c.h
│   ├── f.h
│   ├── j.h
│   └── k.h
├── j.cpp
├── jjk.c
├── k.cpp
├── main.c
└── Makefile
```


```make

include ../../makelib.mak

TOPDIR:=$(call readlink_f,.)

setjjk_DEPS = pre_setjjk
setjjk_POST = post_setjjk
setjjk_DEPS_CLEAN = clean_pre_setjjk
setjjk_SRCS = a.c 
setjjk_SRCS += jjk.c
setjjk_SRCS += k.cpp
setjjk_SRCS += ia.S ib.S
setjjk_SRCS += f.link.c
f_link_c_SRC = f.c
setjjk_SRCS += ic.link.S ibb.link.S
ic_link_S_SRC = ic.S
ibb_link_S_SRC = ibb.S
setjjk_SRCS += j.link.cpp
j_link_cpp_SRC = j.cpp
INCLUDE_FLAGS = -I${TOPDIR}/inc
setjjk_CFLAGS = -Wall -DCFILE=1 ${INCLUDE_FLAGS}
setjjk_CPPFLAGS = -Wall -DCPPFILE=1 ${INCLUDE_FLAGS}
setjjk_LDFLAGS = -Wall -DLDFLILE=1 ${INCLUDE_FLAGS}
setjjk_ASFLAGS = -Wall -DASFILE=1 ${INCLUDE_FLAGS}
d_link_c_SRC = d.c
f_link_cpp_SRC = g.cpp

main_SRCS = main.c b.c c.c
main_CFLAGS = -Wall -DMAIN_CFILE=1 ${INCLUDE_FLAGS}
main_CPPFLAGS = -Wall -DMAIN_CPPFILE=1 ${INCLUDE_FLAGS}
main_LDFLAGS = -Wall -DMAIN_LDFLILE=1 ${INCLUDE_FLAGS}
main_ASFLAGS = -Wall -DMAIN_ASFILE=1 ${INCLUDE_FLAGS}


all:post_setjjk main

post_setjjk: setjjk
    $(call call_exec,${TRUE},"POST","setjjk")

pre_setjjk:
    $(call call_exec,${TRUE},"PRE","setjjk")

clean_pre_setjjk:
    $(call call_exec,${TRUE},"CLEANPRE","setjjk")

clean_post_setjjk:clean_setjjk
    $(call call_exec,${TRUE},"CLEANPOST","setjjk")  

$(eval $(call simple_makefile_exe_whole,setjjk main))

clean:clean_post_setjjk clean_main
```

> run make all

```shell
    DEPS      c.c.d
    DEPS      b.c.d
    DEPS      main.c.d
    LINK      j.link.cpp
    DEPS      j.link.cpp.d
    LINK      ibb.link.S
    DEPS      ibb.link.S.d
    LINK      ic.link.S
    DEPS      ic.link.S.d
    LINK      f.link.c
    DEPS      f.link.c.d
    DEPS      ib.S.d
    DEPS      ia.S.d
    DEPS      k.cpp.d
    DEPS      jjk.c.d
    DEPS      a.c.d
    CC        a.o
    CC        jjk.o
    CPPC      k.o
    AS        ia.o
    AS        ib.o
    CC        f.link.o
    AS        ic.link.o
    AS        ibb.link.o
    CPPC      j.link.o
    PRE       setjjk
    LD        setjjk
    POST      setjjk
    CC        main.o
    CC        b.o
    CC        c.o
    LD        main
```
> it will link file  for the kernel and compile it
> 
```shell
.
├── a.c
├── a.c.d
├── a.o
├── b.c
├── b.c.d
├── b.o
├── c.c
├── c.c.d
├── c.o
├── f.c
├── f.link.c -> f.c
├── f.link.c.d
├── f.link.o
├── gas.sh
├── gcc.sh
├── gpp.sh
├── ia.o
├── ia.S
├── ia.S.d
├── ibb.link.o
├── ibb.link.S -> ibb.S
├── ibb.link.S.d
├── ibb.S
├── ib.o
├── ib.S
├── ib.S.d
├── ic.link.o
├── ic.link.S -> ic.S
├── ic.link.S.d
├── ic.S
├── inc
│   ├── a.h
│   ├── b.h
│   ├── c.h
│   ├── f.h
│   ├── j.h
│   └── k.h
├── j.cpp
├── jjk.c
├── jjk.c.d
├── jjk.o
├── j.link.cpp -> j.cpp
├── j.link.cpp.d
├── j.link.o
├── k.cpp
├── k.cpp.d
├── k.o
├── main
├── main.c
├── main.c.d
├── main.o
├── Makefile
└── setjjk
```

### HOWTO Compile
> just goto makelib directory and make all the result file is makelib.lib






