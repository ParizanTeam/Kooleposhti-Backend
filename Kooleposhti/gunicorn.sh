#!/bin/bash

source /home/ubuntu/.local/share/virtualenvs/Kooleposhti-CSvIaxZK/bin/activate

gunicorn --access-logfile - \
         --workers=5 \
         --bind 127.0.0.1:8000 Kooleposhti.wsgi:application



