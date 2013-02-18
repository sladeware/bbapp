<!--- -*- mode: markdown; coding: utf-8; -*- -->

Bionic Bunny Application Framework

Copyright (c) 2013 Sladeware LLC

http://www.bionicbunny.org/

What is Bionic Bunny Application?
---------------------------------

Bionic Bunny Application or **BBAPP** is a high-level Python framework that
encourages developement of BB based applications. The main goal of BBAPP is to
generate the Bionic Bunny Operating System or
[BBOS](http://github.org/sladeware/bbos/).

All documentation is in the _doc_ directory.

Installation
------------

1. Download the latest version of BBAPP (see http://www.bionicbunny.org):

        $ git clone git@github.com:sladeware/bbapp.git

2. To install bbapp, make sure you have [Python](http://www.python.org/) 2.6 or
   greater installed. If you're in doubt, run:

        $ python -V

3. Run the tests:

        $ python setup.py test

   If some tests fail, this library may not work correctly on your
   system. Continue at your own risk.

4. Run this command from the command prompt to install `bbapp`:

        $ python setup.py install

   All the modules will be installed automatically if required. The installation
   process will generate default config file `~/.bbconfig`. In case you would
   like to refresh it and does not want to reinstall the package, run:

        $ python -m bb.config

> **NOTE:** Developers may use ["development mode"](http://goo.gl/Hoawa) to skip
> direct installation process: `$ python setup.py develop`. Once the work has
> been done you can remove the project source from a staging area using
> `$ python setup.py develop --uninstall`.
