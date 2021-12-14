#!/bin/bash

git checkout deploy

git add .

NOW=$( date + '+%F_%H:%M:%S' )

git commit -m "new deploy at $NOW"

git pull

cd Kooleposhti

source /home/ubuntu/.local/share/virtualenvs/Kooleposhti-CSvIaxZK/bin/activate

pipenv sync

python manage.py makemigrations

python manage.py migrate

cd ..

pip install -r requirements.txt

systemctl restart nginx

systemctl restart gunicorn


