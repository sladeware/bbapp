<!--- -*- mode: markdown; -*- -->

This **helloworld** demo prints `Hello, World!` and demonstrates how to use B3
build system:

    $ b3 build :helloworld
    $ ./helloworld

Complete list of available features:

 * `b3 build :helloworld` -- compiles `helloworld` with help of GCC compiler
 * `b3 build :helloworld-propeller` -- compiles with help of PropGCC compiler
 * `b3 build :helloworld-propeller-load` -- compiles and load propeller binary
