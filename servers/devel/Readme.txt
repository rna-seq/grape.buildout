===============================
Get Started Quickly With Raisin
===============================

Install Python 2.6.6 on your system.

Then install virtualenv like this:

    easy_install virtualenv

Run virtualenv:

    virtualenv --no-site-packages .

Run the bootstrap.py file in your project:

    ./bin/python bootstrap.py

This will install everything necessary in preparation for running the buildout
like this:

    ./bin/buildout

If there are any problems connecting to MySQL, check the settings in the
following file:

  etc/connections/development.ini

Run the Restish instance of Raisin using the Paste HTTP server in the
foreground::

  $ bin/paster serve etc/restish/development.ini

Try out if it is possible to get a resource from the restish server::

  $ curl -i -H "Accept:text/csv" 127.0.0.1:6464/projects

Run the Pyramid instance of Raisin using the Paste HTTP server in the
foreground::

  $ bin/paster serve etc/pyramid/development.ini

Visit the Pyramid test instance of Raisin at::

    http://localhost:7777/

Default login and password are:

login: raisin
password: raisin
