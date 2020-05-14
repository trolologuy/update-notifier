#!/bin/bash
cd /vagrant/

export DEBIAN_FRONTEND=noninteractive

sudo apt-get update -y
# sudo apt-get upgrade -y
# Workaround for the grub-config-prompt issue :
DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
# As taken from here :
# https://askubuntu.com/questions/146921/how-do-i-apt-get-y-dist-upgrade-without-a-grub-config-prompt

# install firefox and geckodriver
sudo apt-get install firefox wget -y
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
sudo tar -xzf geckodriver-v0.26.0-linux64.tar.gz -C /usr/local/bin \
     && rm geckodriver-v0.26.0-linux64.tar.gz \
     && chmod +x /usr/local/bin/geckodriver \
     && export PATH=/usr/local/bin:$PATH

# install the requirements and run the upgrade-notifier
sudo apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    python3-dev \
    python3-lxml \
    python3-pip \
    && pip3 install -r requirements.txt

python3 update-notifier.py -i installed.json