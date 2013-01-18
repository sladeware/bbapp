<!--- -*- mode: markdown; -*- -->

Bionic Bunny Build (B3)
=======================

Bionic Bunny Build or **B3** is a build tool initially created for BB
applications. At a high level, B3 reads build descriptions stored in build
scripts or `BUILD`, constructs a directed acyclic graph (DAG) called image of
targets, and executes a specified set of goals against those targets.

B3 is part of BB framework and so depends on `bb` package. However it doesn't
depend on BB application. The following code snippet shows a simple example of
roboot with body and two arms that we're going to build:

```python
import bb

p1 = PropellerP8X32A_Q44()
p2 = PropellerP8X32A_Q44()
# Build robot board: processors P1, P2
board = Protoboard([p1, p2])

class Body(bb.app.Mapping):
  name_format = "BODY_%(id)"
  threads = [bb.app.Thread("UI", "ui_runner")]
  processor = p1

class Arm(bb.app.Mapping):
  name_format = "ARM_%(id)"
  threads = [bb.app.Thread("")]
  processor = p2

body = Body()
arm1, arm2 = Arm(), Arm()
```

A simple example:

helloworld.py

```python
def helloworld():
  print "Hello world!"
```

```c
#include <stdio.h>

int main() {
  printf("Hello world!")
  return 0;
}
```

BUILD

```python
from helloworld import helloworld

propeller_binary(target = helloworld,
                 srcs = ["helloworld.c"])
```

Compilers and Loaders
---------------------

B3 intends to use a big variaty of compilers and loaders in order to support
wide range of existed microcontrollers and boards.

All the supported compilers are located in `bb.tools.compilers` package and can
be managed by `bb.tools.compiler_manager` manager. Each compiler is derived from
`Compiler` class.

All the loaders are located in `bb.tools.loaders` package and can be managed by
`bb.tools.loader_manager`.

Building
--------

The core object of interest is *target*. A target specifies something that
should be produced by B3. The most useful target is `binary`. BB adds special
target `bb_binary` that automatically adds `bb` dependency.

For each target a *generator* and *image* are created. The image is the objects
container and it is intermediate representation of an application. Generator
converts image into a form (e.g. binary) that can be readily executed by a
machine. In order to build and compile image, the generator uses
*builders*. Builders are one of the primary building blocks of B3 application,
providing build process to generator for a single object of an image. They
guide generator in building, compilation, etc.

> NOTE: BB doesn't have predefined images, thus generator builds image by input
> objects with help of builders.

The following code snippet shows how to write builders for `Body` and `Arm`
classes.

```python
from home_robot import body, arm1, arm2, Body, Arm

class BodyBuilder:

  def gen_config_h(self, body):
    output_fn = self.buildpath(["config.h"])
    with open(output_fn, "w") as output_fh:
      output_fh.write("#define ")

  def on_compile_with_propgcc(self, body, g, compiler):
    compiler.files += ["body.c"]

  on_compile_with_gcc = on_compile_with_propgcc
  on_compile_with_catalina = on_compile_with_propgcc

  def on_compile_with_dynamicc(self, body, g, compiler):
    compiler.files += ["robot_body.c"]

class ArmBuilder:

  def on_compile_with_propgcc(self, arm, g, compiler):
    compiler.files += ["arm.c"]
```

To get list of supported compilers B3 processes builder events such as
`on_compile_with_([\w\_\d]+)$`. Considering `BodyBuilder`, B3 processes
`on_compile_with_propgcc`, `on_compile_with_gcc` and `on_compile_with_dynamicc`
attributes and sees that supported compilers are PropGCC, GCC, Catalina and
Dynamic C.

However there're may be more than one builder for a single object, in case this
builder appears in more than one build-script (this can be useful if you're
going to support more than one programming language).

Once each required object has a builder a build target can be created:

```python
body_binary = bb_binary("body", [body])
arm1_binary = bb_binary("arm1", [arm1])
arm2_binary = bb_binary("arm2", [arm2])
```

Note, here we do not specify compiler directry e.g. ```bb_binary("body", [body],
compiler="propgcc")```, thus B3 will automatically decide which compiler to use
with help of `default_compiler_selector`. In case you would like to choose
compiler from the range of available, you can specify `compiler` argument as a
function. If binary can not be built, an exception occurs.

Loading
-------

Once `Binary` object has been created, you can use loaders from
`bb.tools.loaders` package. Let us continue example above and load
`body_binary` on the board:

```python
parts = ("body", "arm1", "arm2")
for name, i in zip(parts, range(len(parts))):
  propeller_load(name   = "%s-load" % name,
                 binary = "%s" % name,
                 deps   = [":%s" % name],
                 port   = "/dev/ttyUSB%d" % i)
```

The snippet shows that if `body_binary`, `arm1_binary` and `arm2_binary` was
compiled with help of PropGCC compiler, we're using `propler` loader.

In case you need to compile only Propeller binary and then load it,
`propeller_binary` target can be used:

```python
propeller_binary("body", [body], port="/dev/ttyUSB0", terminal_mode=True)
```

Build script
------------

B3 reads build descriptions stored in build scripts `([\w\d\_]+)_build.py`. The
BUILD file has to be imported with help of `import_buildfile` primitive. In this
case module content will be analysed and required dependencies will be loaded
automatically. For instance, let us take a look on BUILD file
`home_robot_build.py` that keeps code snippets above. B3 will take all module
members with `Builder` postfix. Since `BodyBuilder` ends with `Builder` and not
derived from `Builder`, engine will try to find `Body` object. Once `Body` class
has been found, `BodyBuilder` class will be updated, the builder will be
registered and assigned to class `Body`.

B3 has to process build files

```python
b3.process_path("~/myproject")
```

* src/main/java
* src/main/c
* src/main/python
