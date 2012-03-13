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

Raisin expects a MySQL server with the following configuration:

  [raisin]
  port = 3306
  server = 127.0.0.1
  user = raisin
  password = raisin

You will probably have to change this for your configuration, and you can
do so by changing the settings in this file:

  etc/connections/mysql.ini

= Starting the servers =

Run supervisor in the foreground:

    ./bin/supervisord -e debug -n -c etc/supervisor/supervisord.conf

If everything works fine, run supervisor in daemon mode:

    ./bin/supervisord -c etc/supervisor/supervisord.conf

You can access the supervisor status page here and stop and start servers:

    http://127.0.0.1:9001

Or you can see the status on the command line:

    ./bin/supervisorctl -c etc/supervisor/supervisord.conf status

And then do all the starting and stopping from the command line:

You can stop the restish server:

    ./bin/supervisorctl -c etc/supervisor/supervisord.conf stop restish

You can stop the pyramid server

    ./bin/supervisorctl -c etc/supervisor/supervisord.conf stop pyramid

You can start the restish server:

    ./bin/supervisorctl -c etc/supervisor/supervisord.conf start restish

You can start the pyramid server

    ./bin/supervisorctl -c etc/supervisor/supervisord.conf start pyramid

You can stop all servers

    ./bin/supervisorctl -c etc/supervisor/supervisord.conf stop all

You can start all servers

    ./bin/supervisorctl -c etc/supervisor/supervisord.conf start all

You can also restart all servers:

    ./bin/supervisorctl -c etc/supervisor/supervisord.conf restart all

= Accessing the Pyramid server =

Visit the Pyramid test instance of Raisin at::

    http://localhost:7777/project/Test/tab/experiments/

Default login and password are:

    login: raisin
    password: raisin

= Accessing the restish server =

Try out if it is possible to get a resource from the restish server::
 
    curl -i -H "Accept:text/csv" 127.0.0.1:6464/projects

= Starting the servers without supervisor = 

Run the Restish instance of Raisin using the Paste HTTP server in the
foreground::

    ./bin/paster serve etc/restish/development.ini
 
Run the Pyramid instance of Raisin using the Paste HTTP server in the
foreground::

    ./bin/paster serve etc/pyramid/development.ini

Run Restish in daemon mode:

    ./bin/paster serve etc/restish/production.ini --daemon --pid-file=restish.pid --log-file=restish.log 

Run Pyramid in demon mode
    
    ./bin/paster serve etc/pyramid/production.ini --daemon --pid-file=pyramid.pid --log-file=pyramid.log 
