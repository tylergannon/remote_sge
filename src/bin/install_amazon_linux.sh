# Installer needs to do:
#   * Ensure that python prerequisites are installed.
#   * Install latest version of python

#   * Install pyenv
#   * create virtualenv

VERSION=3.6.4


curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash

export PATH="/home/ec2-user/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

cat << EOF >> $HOME/.bashrc
export PATH="/home/ec2-user/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF
#   * Ensure that readline is there for Python.  We don't care about sqlite3.
sudo yum -y install readline-devel
#   * Install our Python (3.6.4)
pyenv install $VERSION

pyenv virtualenv $VERSION remote_sge
echo 'remote_sge' > .python-version

if [[ `python --version` != "Python ${VERSION}" ]]; then
    echo "Expected Python ${VERSION} but got `python --version`."
    echo "Exiting."
    exit 1
fi



# okay what is missing.
# * Set up the nginx virtual server.
# * Make sure nginx is started.
# * Set up startup scripts for gunicorn