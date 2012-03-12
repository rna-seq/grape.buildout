===============================
Get Started Quickly With Raisin
===============================

Install Python 2.6.6 on your system.

Then install virtualenv like this:

    easy_install virtualenv

Go to the devel folder and run virtualenv:

    cd devel
    virtualenv --no-site-packages .

Run the bootstrap.py file in your project:

    ./bin/python bootstrap.py

This will install everything necessary in preparation for running the buildout
like this:

    ./bin/buildout

If there are any problems connecting to MySQL, check the settings in the
following file:

    etc/connections/development.ini

Run supervisor in the foreground:

    ./bin/supervisord -e debug -n -c etc/supervisor/supervisord.conf

If everything works fine, run supervisor in daemon mode:

    ./bin/supervisord -c etc/supervisor/supervisord.conf

Visit the Pyramid test instance of Raisin at::

    http://localhost:7777/

Default login and password are:

login: raisin
password: raisin
