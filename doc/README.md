<!--- -*- mode: markdown -*- --->

You must install [pyserial](http://pypi.python.org/pypi/pyserial) and `sphinx`
to build this documentation:

    $ sudo apt-get install python-sphinx python-serial

Please run the following command in order to generate docs in html format:

    $ make html

Note that the results are under build/html. Also, the index.html there may not
contain all of the documentation and so you should keep digging around in the
subdirectories if you think more docs _might_ be found. No one will complain
if you fix this ;)
