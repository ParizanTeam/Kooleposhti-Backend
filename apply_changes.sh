#!/bin/bash

git pull

systemctl restart nginx

systemctl restart gunicorn


