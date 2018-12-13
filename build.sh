#!/bin/bash

sudo git push --repo git://github.com/sirisurab/dupquest.git origin master

docker build -t sirisurab/dq-app --no-cache git@github.com:sirisurab/dupquest.git

docker login -u sirisurab -p everestK2

docker push sirisurab/dq-app
