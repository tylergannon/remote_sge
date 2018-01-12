# Installer needs to do:
#   * Ensure that python prerequisites are installed.
#   * Install latest version of python

#   * Install pyenv
#   * create virtualenv

VERSION=3.6.4

echo "Installing pyenv."
sudo yum install git
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

cat << EOF >> $HOME/.bashrc
export PATH="$HOME/.pyenv/bin:\$PATH"
eval "\$(pyenv init -)"
eval "\$(pyenv virtualenv-init -)"
EOF
#   * Ensure that readline is there for Python.  We don't care about sqlite3.
[[ -z "$DOCKER" ]] && [[ ! -z `which yum 2>/dev/null` ]] && echo "Installing readline-devel" && sudo yum -y install readline-devel
[[ ! -z `which pacman 2>/dev/null` ]] && echo "not installing readline" && echo "`pacman -Q readline` is installed"
#   * Install our Python ($VERSION)
echo "Installing Python $VERSION"
pyenv install $VERSION

echo "Creating virtualenv called remote_sge."
pyenv virtualenv $VERSION remote_sge
pyenv activate remote_sge
if [[ `python --version` != "Python ${VERSION}" ]]; then
    echo "Expected Python ${VERSION} but got `python --version`."
    echo "Exiting."
    exit 1
fi

cat << EOF


Okay initial tools installed.  Please restart your shell or else paste the following:

export PATH="\$HOME/.pyenv/bin:\$PATH"
eval "\$(pyenv init -)"
eval "\$(pyenv virtualenv-init -)"

Activate Python $VERSION by typing \`pyenv activate remote_sge\`.
To automatically activate it in a given directory, cd to that location and type:

\$ echo remote_sge > .python-version

Once activated you can proceed with 'python -m sge_server.install'"

EOF

# okay what is missing.
# * Set up the nginx virtual server.
# * Make sure nginx is started.
# * Set up startup scripts for gunicorn