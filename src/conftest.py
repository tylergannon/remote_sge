import os
from configparser import ConfigParser
import pytest

os.environ['SGE_ROOT'] = '/opt'
os.environ['SGE_ARCH'] = 'amd64'

@pytest.fixture
def job_package_str():
    "Returns a string representation of packaged job with sleeper.sh inside."
    return('H4sIACe8WVoC/+3SsQrCMBSF4TvnKSLuNk3S5nXaakqFotK0g29vrOCok6Lwf8vhwlkO3DTGeInTL' +
           'g3yMSarvV8z1NWaxj7ulbdSOmurUAZfBzGlc74SbeQLljS3k9YyX8c4vejlWt+/GZk9809sN0V3PB' +
           'Vdmwal0v0ZtDMq7oezbg7tHBslAAAAAAAAAAAAAAAAAIAfdAN+v52WACgAAA==')

@pytest.fixture
def sample_config():
    return ConfigParser("""###################################################################
#    Remote SGE settings
#
#    This file will be placed at $dest_path
#
#    note that if there is an NGinx frontend, the client's ip,
#    address settings will not be the same as those for gunicorn.
#
####################################################################
[client]
host = remote-sge-host
port = 443
client_certificate = None

[general]
shell = /bin/bash

[server]
#  The location where jobs in progress will be kept.
#  Each job will be unpacked into a subdirectory of work_root,
#  and that path will be given to SGE as the working directory.
work_root=$$HOME/.local/remote_sge/work

#   The location where finished, archived jobs will go.
#   This will also be the path pointed to by nginx virtual server,
#   for retrieving completed jobs.
completed_files_root=$$HOME/.local/remote_sge/finished

job_wrapper=
# Can also specify ip_address:port
# http://nginx.org/en/docs/http/ngx_http_core_module.html#listen
nginx_listen=443
# Set this to a valid name if there are multiple virtual servers.
nginx_server_name=_
#   The ip address/port, or unix domain socket that the wsgi will use.
wsgi_binding=unix:/tmp/remote_sge.sock

[qsub_settings]
# where to put output files, omit to leave them in the working directory.
output_path=
join_stdout_and_stderr=yes
command_shell=/bin/bash
# e.g. smp 4 or orte 4
parallel_environment= smp 4
binary_executable=no
# leave empty to submit into the primary queing mechanism
default_queue=
# whether to interpret the executable through 'command_shell'
exec_in_shell=yes

[qsub_parameters]
# additional raw qsub parameters could be added,
# in the form:
# -j=y

[command_environment]
# Environment variables to set for each job.
VAR1=castlevania iv
VAR2=supermariokart
""")
