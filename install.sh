#!/usr/bin/env bash

# Download Python 3.5.2
wget 'https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz'
cd Python-3.5.2

# Install libssl-dev required for pip3.5
sudo apt-get install libssl-dev


# Install Python 3.5.2
./configure
make
sudo make install

# Install virtualenvwrapper
sudo pip3.5 install virtualenvwrapper
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=$(which python3.5)

# Creating a virtualenv
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv --no-site-packages --python=$(which python3.5)

# Installing rfid
cd ..
cd rfid
pip install .

# Installing blackfield
cd ..
cd blackfield
pip install .


