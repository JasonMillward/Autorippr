#!/bin/bash

# Install Script Version 1.0
# This script is designed to install Autorippr for Ubuntu 16.04 LTS
# All required dependancies and packages will be installed
# Packages that are installed:
# --GIT
# --Makemkv
# --Python Dev Tools
# --Python Dependancies for Autorippr
# --PIP
# --Handbrake-CLI
# --Filebot
# --Autorippr

# Change to execution directory
cd ~

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
sudo python get-pip.py

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
sudo apt-get install python-dev

# Install Filebot
sudo apt-get --assume-yes install oracle-java8-installer
if [ `uname -m` = "i686" ]
then
   wget -O filebot-i386.deb 'http://filebot.sourceforge.net/download.php?type=deb&arch=i386'
else
   wget -O filebot-amd64.deb 'http://filebot.sourceforge.net/download.php?type=deb&arch=amd64'
fi
sudo dpkg --force-depends -i filebot-*.deb && rm filebot-*.deb

# Install Python Required Packages
sudo pip install tendo pyyaml peewee

# Install Autorippr
cd ~
git clone https://github.com/JasonMillward/Autorippr.git
cd Autorippr
git checkout
cp settings.example.cfg settings.cfg

# Verification Test
python autorippr.py --test

# Completion Message
echo " "
echo "###################################################"
echo "##            Install Complete!                  ##"
echo "##      Update: ~/Autorippr/settings.cfg         ##"
echo "###################################################"
