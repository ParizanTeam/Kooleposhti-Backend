
#!/bin/bash
#
# auto_commit.sh - git commit all changes as they happen
#
git commit -a -m "autoupdate `date +%F-%T`"
git pull heroku_logger master
git push heroku_logger master
