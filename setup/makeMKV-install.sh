#!/bin/bash

key=""
makemkv_dir="$HOME/.MakeMKV"
settings_file="$makemkv_dir/settings.conf"
makemkv_path="http://www.makemkv.com/download"

# Make sure root can not run our script
if [ $EUID == 0 ]; then
    echo "This script must not be run as root" 1>&2
    exit 1
fi


curr_version=$(wget -qO- $makemkv_path | grep -m 1 "MakeMKV v" | sed -e "s/.*MakeMKV v//;s/ (.*//")

if [[ -z "$curr_version" ]]; then
    echo "Could not scrape current version for MakeMKV" 1>&2
    exit 1
else
    echo "Scraped the MakeMKV download page and found the latest version as" ${curr_version}
fi


bin_zip=makemkv-bin-${curr_version}.tar.gz
oss_zip=makemkv-oss-${curr_version}.tar.gz
oss_folder=makemkv-bin-${curr_version}
bin_folder=makemkv-oss-${curr_version}


echo "Downloading required zip files"
cd /tmp/

wget http://www.makemkv.com/download/$bin_zip
wget http://www.makemkv.com/download/$oss_zip

tar -xzf $bin_zip
tar -xzf $oss_zip

cd $oss_folder
make -f makefile.linux
sudo make -f makefile.linux install

cd ../$bin_folder
make -f makefile.linux
sudo make -f makefile.linux install

cd ..

echo removing downloaded files
rm $bin_zip
rm $oss_zip
rm -rf $oss_folder
rm -rf $bin_folder


if [ ! "$key" ]; then
    echo
    echo "Please enter MakeMKV License Key [none]:"
    read key
fi

if [ "$key" ]; then
    if [ -e $settings_file ]; then
        if grep -q app_Key $settings_file; then
            existing_key=$(grep app_Key $settings_file | \
                awk -F\" '{ print $2 }')

            if [ ! "$key" == "$existing_key" ]; then
                sed -e 's,app_Key.*,'app_Key\ =\ \"$key\"',g' "$settings_file" > \
                    $settings_file.new

                mv $settings_file.new $settings_file
            fi
        fi
    else
        mkdir -p $makemkv_dir
        echo 'app_Key = "'$key'"' > $settings_file
    fi
fi
