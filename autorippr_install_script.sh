#!/bin/bash

# Ubuntu 16.04 Error fix for installing packages
sudo apt-get purge runit
sudo apt-get purge git-all
sudo apt-get purge git
sudo apt-get autoremove
sudo apt update

# Install Git
sudo apt install git 

#Install PIP
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

#Install Makemkv
wget http://www.makemkv.com/download/makemkv-bin-1.10.0.tar.gz
wget http://www.makemkv.com/download/makemkv-oss-1.10.0.tar.gz
tar -zxmf makemkv-oss-1.10.0.tar.gz
tar -zxmf makemkv-bin-1.10.0.tar.gz
cd makemkv-oss-1.10.0
./configure
make
sudo make install
cd ..
cd makemkv-bin-1.10.0
make
sudo make install

# Install Handbrake CLI
sudo apt-get install handbrake-cli

# Python update to enable next step
sudo apt-get pthyon-dev

# Install Python Required Packages
sudo pip install tendo pyyaml peewee

# Install Autorippr
cd ~
git clone https://github.com/JasonMillward/Autorippr.git
cd Autorippr
git checkout
cp settings.example.cfg settings.cfg

# Verification Test
command python autorippr.py --test

# Completion Message
echo "Install Complete, don't forget to configure settings.cfg!"
