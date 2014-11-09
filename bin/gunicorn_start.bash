#!/bin/bash

NAME="concerns_app"                                  # Name of the application
DJANGODIR=/var/django/crowdconcerns.com/concernsprj             # Django project directory
SOCKFILE=/var/django/crowdconcerns/run/gunicorn.sock  # we will communicte using this unix socket
USER=prob                                        # the user to run as
GROUP=webapps                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=concernsprj.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=concernsprj.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
#source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
 # --bind=unix:$SOCKFILE \
  --bind=127.0.0.1:8000 \