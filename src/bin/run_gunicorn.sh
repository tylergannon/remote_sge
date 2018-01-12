#!/bin/bash

echo "Starting server."

# Create the run directory if it doesn't exist
# RUNDIR=$(dirname $SOCKFILE)
# test -d $RUNDIR || mkdir -p $RUNDIR

SCRIPT_NAME=restful_sge/gunicorn_config.py
INSTALLED_CFG=`python -c "import site; print(site.PREFIXES[0])"`/etc/restful_sge

if [ "install_conf" == "$1" ]; then
    DEST="/home/$USER/.config/restful_sge"
    echo "Copying configuration files to $DEST."
    mkdir -pv "$DEST"
    for file in `find $INSTALLED_CFG -type f -not -path "**/__pycache__/**"`; do
        cp -v "$file" "$DEST"
    done
else
    if [ -e "/etc/$SCRIPT_NAME" ]; then
        CONFIG="/etc/$SCRIPT_NAME"
    elif [ -e "/home/$USER/.config/$SCRIPT_NAME" ]; then
        CONFIG="/home/$USER/.config/$SCRIPT_NAME"
    else
        CONFIG="$INSTALLED_CFG/gunicorn_config.py"
    fi

    echo "Starting server using $CONFIG"

    exec gunicorn restful_sge:app -m 0007 -c "$CONFIG"
fi
