# Restful front end for SGE Gridengine

A basic Flask application that exposes common SGE tasks to enable remote users to:

* Submit a job
* Check on job status
* Download a .tgz file with job results

A client component that wraps restful API into a Python class.

Sample conf file: https://gist.github.com/tylergannon/ad2bb900ec7f17a2be9f4fcb1e68f8f3

```python

client = SgeClient('my-sge-host', port=8080, cert='~/keys/me@host.pem')
job_info = client.submit('do_mega_heavy_business.sh')

# ... later on ...

job_list = client.list_active_jobs(queue='some_queue')
job_status = client.job_status(job_info.job_id)
if type(job_status) is CompletedJob:
    job_status.extract_results('~/my_jobs/')

```

## About Security

**Important note: if left running on a port that's available to the internet, anyone out there will have unfettered access to run jobs on your grid.**

This package is designed around two possible security models:

1. SSH tunnel.  You configure RestfulSGE to listen to a port on the loopback IP address, and the SgeClient will use your SSH config settings (which should involve an IdentityFile) to open up a secure tunnel for the API calls.
2. Client Certificate.  You **still** configure RestfulSGE to listen on 127.0.0.1, then configure an NGinx front end that requires a client certificate (and probably also an IP Address whitelist).


## Installation

### Ensure development headers are installed.

Debian:

```
sudo apt-get -y install libsqlite3-dev libreadline-dev libbz2-dev zlib1g-dev openssl libssl-dev libncurses5-dev libncursesw5-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev curl gridengine-drmaa-dev git
```

Amazon Linux / CentOS:



```
sudo yum -y install readline-devel bzip2-devel gcc gcc-c++ kernel-devel make zlib-devel openssl-devel
```

### Install pyenv and python


```

./install.sh

#  Or, do the following.

curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash

pyenv install 3.6.4

PYENV_HOME=~/.pyenv
mkdir -p $PYENV_HOME

echo "3.6.4" > $PYENV_HOME/version

python --version  # should be 3.6.4


```

Notice any warnings returned by pyenv installer.  You may need to install other developmment libraries and then reinstall Python.

### Configure application

```
cd sge_job_commuter
pipenv install
```

## Other Stuff

```bash
tar -cvzf bar.baz.tgz *.foo
```

# Troubleshooting

## Server won't start

If the server quits immediately with errors about not being able to find something,

### Verify that DRMAA_LIBRARY_PATH is properly set.

On amazon linux, it's set wrong in `/etc/profile.d/sge.sh`.  
Open that file and set the value to the result given by `find /opt/sge -name "libdrmaa.so.1"`

