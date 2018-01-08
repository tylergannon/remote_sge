"""
* $RESTFUL_SGE_CONFIG environment variable
* ~/.config/restful_sge/config.py
* /etc/restful_sge/config.py

# Gunicorn only cares about the variables set at the very bottom of the file.
# Restful SGE Client settings can also be provided at the time of object creation.

"""
from os.path import dirname, join, abspath

#########################################################
#
#                 gunicorn settings
#
#########################################################

name = "restful_sge"
# BIND="unix:~/FLASK/sock"
bind = "127.0.0.1:8080"
user='tyler'
group="tyler"
workers=4
logconfig = abspath(join(dirname(__file__), 'logging.conf'))
