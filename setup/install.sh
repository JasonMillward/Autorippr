#!/bin/sh

# Author:   mechevar
# URL:      http://www.makemkv.com/forum2/viewtopic.php?f=3&t=5266

sudo add-apt-repository ppa:stebbins/handbrake-releases
sudo apt-get update
sudo apt-get python install build-essential libc6-dev libssl-dev libexpat1-dev libgl1-mesa-dev libqt4-dev g++ python-imdbpy handbrake-cli

cd /tmp/
wget "http://www.makemkv.com/download/"
export curr_version=$(grep -m 1 "MakeMKV v" index.html | sed -e "s/.*MakeMKV v//;s/ (.*//")

echo "Scraped the MakeMKV download page and found the latest version as" ${curr_version}

export bin_zip=makemkv-bin-${curr_version}.tar.gz
export oss_zip=makemkv-oss-${curr_version}.tar.gz
export oss_folder=makemkv-bin-${curr_version}
export bin_folder=makemkv-oss-${curr_version}

wget http://www.makemkv.com/download/$bin_zip
wget http://www.makemkv.com/download/$oss_zip

tar -xzvf $bin_zip
tar -xzvf $oss_zip

cd $oss_folder
make -f makefile.linux
sudo make -f makefile.linux install

cd ../$bin_folder
make -f makefile.linux
sudo make -f makefile.linux install

cd ..

echo removing downloaded files
rm index.html
rm $bin_zip
rm $oss_zip
rm -rf $oss_folder
rm -rf $bin_folder