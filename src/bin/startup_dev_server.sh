#!/bin/bash

docker build -t tylergannon/gridengine .

docker stop $(docker ps -aq)

docker run -p 127.0.0.1:10022:22 -h gridengine.test \
    -p 127.0.0.1:4443:443 \
    --mount type=bind,source="$(pwd)",target=/var/remote_sge \
    --rm -d --name gridengine tylergannon/gridengine
sleep 1
ssh -p 10022 testuser@localhost

pyenv activate remote_sge

export DOCKER=yes

cd /var/remote_sge
export PYTHONPATH=.
export PYENV_VERSION=3.6.4
python sge_server/install.py -i
