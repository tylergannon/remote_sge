#!/bin/bash

docker stop $(docker ps -aq)

docker run -p 127.0.0.1:10022:22 -h gridengine.test \
    --rm -d --name gridengine tylergannon/gridengine

ssh -p 10022 testuser@localhost

DOCKER=yes
