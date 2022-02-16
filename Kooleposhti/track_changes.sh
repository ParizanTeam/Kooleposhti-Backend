#!/bin/bash
git init
git remote add heroku_logger https://${GIT_TOKEN}@github.com/ParizanTeam/Track-Changes.git
git config user.name "heroku"
git config user.email "heroku@example.com"
git pull heroku_logger master
