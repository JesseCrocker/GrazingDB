#!/bin/bash

PIDFILE=/home/deploy/django.pid
kill -9 `cat $PIDFILE`

sleep 10
python /home/deploy/grazingDB/webapp/manage.py run_gunicorn --daemon -w 3 -p $PIDFILE
